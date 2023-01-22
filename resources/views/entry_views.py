from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from ..models import Entry, Glossary
from ..forms.entry_forms import EntryCreateForm, EntryUpdateForm


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = "entry_detail.html"


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryCreateForm
    template_name = "entry_create.html"

    def form_valid(self, form):
        new_entry = form.save(commit=False)
        new_entry.created_by = self.request.user
        new_entry.updated_by = self.request.user

        # If a new glossary is to be created for this entry.
        new_glossary_title = form.cleaned_data.get("new_glossary")
        if new_glossary_title:
            new_glossary = Glossary(
                title=new_glossary_title,
                type="glossary",
                created_by=self.request.user,
                updated_by=self.request.user,
            )
            new_glossary.save()
            new_entry.glossary = new_glossary

        new_entry.save()

        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return HttpResponseRedirect(previous_url)

        return HttpResponseRedirect(reverse_lazy("home"))

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(EntryCreateView, self).post(request, *args, **kwargs)


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryUpdateForm
    template_name = "entry_update.html"

    def form_valid(self, form):
        """
        Sets the updated_by field to the current user, and sets the previous url
        as the success url if previous_url is present.
        """

        updated_entry = form.save(commit=False)
        updated_entry.updated_by = self.request.user
        updated_entry.save()

        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return HttpResponseRedirect(previous_url)

        return HttpResponseRedirect(reverse_lazy("home"))

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(EntryUpdateView, self).post(request, *args, **kwargs)


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = "entry_delete.html"

    def get_success_url(self):
        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return previous_url

        return reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(EntryDeleteView, self).post(request, *args, **kwargs)
