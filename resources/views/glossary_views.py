import csv

from django.utils import timezone
from django.views.generic import View, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms.entry_forms import EntryAddToGlossaryForm
from ..forms.glossary_forms import GlossaryForm, GlossaryUploadForm
from ..models import Entry, Glossary


class GlossaryUploadView(LoginRequiredMixin, View):
    form_class = GlossaryUploadForm
    template_name = "glossary_upload.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # Create new Glossary obj or append to existing Glossary obj
            glossary_obj = create_or_append(request, form)
            build_entries(glossary_obj, request)
            return HttpResponseRedirect(glossary_obj.get_absolute_url())

        return render(request, self.template_name, {"form": form})


def create_or_append(request, form):
    """
    Helper method for GlossaryUploadView. Either creates a new Glossary
    object or gets the Glossary object with which the uploaded data is to be
    associated.
    """

    existing_glossary_obj = form.cleaned_data["existing_glossary"]

    if existing_glossary_obj:
        glossary_obj = Glossary.objects.get(title__iexact=existing_glossary_obj.title)
        glossary_obj.glossary_file = form.cleaned_data["glossary_file"]
        new_notes = form.cleaned_data["notes"]
        if new_notes:
            if glossary_obj.notes:
                glossary_obj.notes = glossary_obj.notes + "\n" + new_notes
            else:
                glossary_obj.notes = new_notes
        glossary_obj.updated_by = request.user
        glossary_obj.save()

    else:
        glossary_obj = Glossary(
            glossary_file=form.cleaned_data["glossary_file"],
            title=form.cleaned_data["new_glossary"],
            notes=form.cleaned_data["notes"],
            created_by=request.user,
            updated_by=request.user,
            type="glossary"
        )
        glossary_obj.save()

    return glossary_obj


def build_entries(glossary_obj, request):
    """
    Helper method for GlossaryUploadView.
    Builds Entry objects from the content of an uploaded text file.
    Receives new Glossary object.
    """

    new_entries = []

    # Regular open() used here to make it possible to set the encoding.
    # Otherwise, if FileField.open() is used, receive following error with
    # Windows text files.
    # > 'cp932' codec can't decode byte 0xef

    with open(glossary_obj.glossary_file.path, encoding="utf-8") as f:

        reader = csv.reader(f, delimiter="\t")

        # Loop for creating new Entry objects from content of uploaded file
        for row in reader:

            # Each row should contain 2 or 3 elements, otherwise ignored
            if (len(row) == 2) or (len(row) == 3):

                # Handling for optional notes item
                if len(row) == 3:
                    notes = row[2]
                else:
                    notes = ""

                # Create Entry object and append to new_entries list
                new_entry = Entry(
                    source=row[0],
                    target=row[1],
                    glossary=glossary_obj,
                    notes=notes,
                    created_on=timezone.now(),
                    created_by=request.user,
                    updated_on=timezone.now(),
                    updated_by=request.user,
                )
                new_entries.append(new_entry)

        # Add all new Entry objects to the database in one write
        Entry.objects.bulk_create(new_entries)

    # Delete the uploaded text file after new Entry objects have been saved to DB
    glossary_obj.glossary_file.delete()


class GlossaryDetailView(LoginRequiredMixin, DetailView):
    model = Glossary
    template_name = "glossary_detail.html"

    def get_context_data(self, **kwargs):
        context = super(GlossaryDetailView, self).get_context_data(**kwargs)
        num_of_entries = context["glossary"].entries.all().count()
        context.update({
            "num_of_entries": num_of_entries,
        })
        return context


class GlossaryCreateView(LoginRequiredMixin, CreateView):
    model = Glossary
    form_class = GlossaryForm
    template_name = "glossary_create.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.type = "glossary"
        obj.save()

        """
        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return HttpResponseRedirect(previous_url)
        """
        return HttpResponseRedirect(obj.get_absolute_url())

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(GlossaryCreateView, self).post(request, *args, **kwargs)


class GlossaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Glossary
    template_name = "glossary_delete.html"
    success_url = reverse_lazy("home")


class GlossaryAddEntryView(LoginRequiredMixin, CreateView):
    """
    Class to add a new Entry object to an existing Glossary Object.
    Called from the Glossary detail page.
    Receives pk of Glossary object in question and sets this for the
    entry.glossary field.
    """

    model = Entry
    form_class = EntryAddToGlossaryForm
    template_name = "glossary_add_entry.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.glossary = Glossary.objects.get(pk=self.kwargs["glossary"])
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()

        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return HttpResponseRedirect(previous_url)

        return HttpResponseRedirect(obj.get_absolute_url())

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(GlossaryAddEntryView, self).post(request, *args, **kwargs)


class GlossaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Glossary
    template_name = "glossary_update.html"
    form_class = GlossaryForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class GlossaryAllEntryView(LoginRequiredMixin, DetailView):
    model = Glossary
    template_name = "glossary_all.html"

    def get_context_data(self, **kwargs):
        context = super(GlossaryAllEntryView, self).get_context_data(**kwargs)
        all_entries = context["glossary"].entries.all()
        num_of_entries = context["glossary"].entries.all().count()
        context.update({
            "all_entries": all_entries,
            "num_of_entries": num_of_entries,
        })
        return context


"""
class GlossaryExportView(LoginRequiredMixin, View):
    form_class = GlossaryExportForm
    template_name = "glossary_export.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):

        # If the cancel button has been pressed in the form, return to the previous URL
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)

        form = self.form_class(request.POST)
        if form.is_valid():
            glossaries = form.cleaned_data.get("glossaries")  # Glossary objects to be exported
            response = build_download(glossaries)
            return response

        return render(request, self.template_name, {"form": form})


def build_download(glossaries):

    # Helper function for GlossaryExportView.
    # Receives list of Glossary objects.
    # Converts each object into a text file.
    # Zips all the text files together.
    # Returns a FileResponse that causes the browser to download the zip file.

    # Create local temporary folder to hold glossary files to be exported
    export_folder = "to_export/"
    if not os.path.isdir(export_folder):
        os.makedirs(export_folder)

    # Create one tab-delim text file for each Glossary object and save to temporary folder
    for glossary in glossaries:
        filename = export_folder + glossary.title + ".txt"
        with open(filename, "w") as f:
            for entry in glossary.entries.all():
                f.write(entry.source + "\t" + entry.target)
                if entry.notes:
                    # Replace any newline and carriage return chars and append note
                    new_note = entry.notes.replace("\r", " ")
                    new_note = new_note.replace("\n", " ")
                    new_note = new_note.replace("  ", " ")
                    f.write("\t" + new_note)
                f.write("\n")

    # Create single zip file from all files created
    shutil.make_archive(base_name="exported_files",  # Name of the zip file to create
                        format="zip",
                        root_dir=export_folder)  # Path of the directory to compress

    # Add zip file to response
    download_target = "exported_files.zip"
    response = FileResponse(open(download_target, "rb"), as_attachment=True)
    # Force browser to download
    response["Content-Disposition"] = "filename=exported_files"

    # Delete local temporary folder containing created glossary files
    shutil.rmtree(export_folder)
    # Delete local zip file
    os.remove(download_target)

    return response
"""
