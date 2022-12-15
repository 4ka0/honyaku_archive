from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from ..models import Entry
from ..forms import EntryCreateForm, EntryUpdateForm


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = "entry_detail.html"


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryCreateForm
    template_name = "entry_create.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()

        # Sets user data on Glossary object if new Glossary is being created with the new Entry
        if obj.glossary.created_by is None and obj.glossary.updated_by is None:
            obj.glossary.created_by = self.request.user
            obj.glossary.updated_by = self.request.user
            obj.glossary.type = "glossary"
            obj.glossary.save()

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
            return super(EntryCreateView, self).post(request, *args, **kwargs)


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryUpdateForm
    template_name = "entry_update.html"

    def form_valid(self, form):
        """ Sets the updated_by field to the current user, and sets the
            previous url as the success url if previous_url is present."""
        obj = form.save(commit=False)
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
