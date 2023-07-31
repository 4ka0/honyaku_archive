import csv

from django.utils import timezone
from django.views.generic import View, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms.glossary_forms import GlossaryForm, GlossaryUploadForm
from ..models import Resource, Item


class GlossaryCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = GlossaryForm
    template_name = "glossary_create.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.resource_type = "GLOSSARY"
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(GlossaryCreateView, self).post(request, *args, **kwargs)


class GlossaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    template_name = "glossary_update.html"
    form_class = GlossaryForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class GlossaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = "glossary_delete.html"
    success_url = reverse_lazy("home")


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
            resource_obj = append_or_create(request, form)
            build_entries(resource_obj, request)
            return HttpResponseRedirect(resource_obj.get_absolute_url())

        return render(request, self.template_name, {"form": form})


def append_or_create(request, form):
    """
    Helper method for GlossaryUploadView.
    Either returns an existing Resource object to which the uploaded data
    is to be appended, or creates and returns a new Resource object with which
    the uploaded data is to be associated.
    """

    existing_resource_obj = form.cleaned_data["existing_glossary"]

    if existing_resource_obj:
        existing_resource_obj.upload_file = form.cleaned_data["upload_file"]
        new_notes = form.cleaned_data["notes"]
        if new_notes:
            if existing_resource_obj.notes:
                existing_resource_obj.notes = (
                    existing_resource_obj.notes + "\n" + new_notes
                )
            else:
                existing_resource_obj.notes = new_notes
        existing_resource_obj.updated_by = request.user
        existing_resource_obj.save()
        return existing_resource_obj

    new_resource_obj = Resource(
        upload_file=form.cleaned_data["upload_file"],
        resource_type="GLOSSARY",
        title=form.cleaned_data["title"],
        notes=form.cleaned_data["notes"],
        created_by=request.user,
        updated_by=request.user,
    )
    new_resource_obj.save()
    return new_resource_obj


def build_entries(resource_obj, request):
    """
    Helper method for GlossaryUploadView.
    Receives Resource object.
    Builds Item objects from the content of an uploaded text file, and
    associates these with the Resource object.
    """

    new_items = []

    # Regular open() used here to make it possible to set the encoding.
    # Otherwise, if FileField.open() is used, receive following error with
    # Windows text files.
    # > 'cp932' codec can't decode byte 0xef

    with open(resource_obj.upload_file.path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")

        # Loop for creating new Entry objects from content of uploaded file.
        for row in reader:
            # Each row should contain 2 or 3 elements, otherwise ignored.
            if (len(row) == 2) or (len(row) == 3):
                # Handling for optional notes item
                if len(row) == 3:
                    notes = row[2]
                else:
                    notes = ""

                # Create Entry object and append to new_entries list.

                # ADD SOME FORM OF VALIDATION HERE
                # DONT JUST SAVE TO THE DB

                # form = EntryForm(row)
                # if form.is_valid():
                #     new_entries.append(new_entry)

                new_item = Item(
                    resource=resource_obj,
                    source=row[0],
                    target=row[1],
                    notes=notes,
                    created_on=timezone.now(),
                    created_by=request.user,
                    updated_on=timezone.now(),
                    updated_by=request.user,
                )
                new_items.append(new_item)

        # Add all new Entry objects to the database in a single write.
        Item.objects.bulk_create(new_items)

    # Delete the uploaded text file, no longer needed.
    resource_obj.upload_file.delete()


"""
# Nolonger needed.
# Replaced with ResourceDetailView.

class GlossaryDetailView(LoginRequiredMixin, DetailView):
    model = Glossary
    template_name = "glossary_detail.html"

    def get_context_data(self, **kwargs):
        context = super(GlossaryDetailView, self).get_context_data(**kwargs)
        num_of_entries = context["glossary"].entries.all().count()
        context.update(
            {
                "num_of_entries": num_of_entries,
            }
        )
        return context
"""


"""
class GlossaryAllEntryView(LoginRequiredMixin, DetailView):
    model = Glossary
    template_name = "glossary_all.html"

    def get_context_data(self, **kwargs):
        context = super(GlossaryAllEntryView, self).get_context_data(**kwargs)
        all_entries = context["glossary"].entries.all()
        num_of_entries = context["glossary"].entries.all().count()
        context.update(
            {
                "all_entries": all_entries,
                "num_of_entries": num_of_entries,
            }
        )
        return context
"""


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
