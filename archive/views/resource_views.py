from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from ..forms.glossary_forms import GlossaryForm
from ..forms.translation_forms import TranslationUpdateForm
from ..models import Resource


class ResourceCreateView(LoginRequiredMixin, CreateView):
    """
    Class to create a new resource. Since translations are only ever uploaded,
    this is only used to create new glossaries.
    """
    model = Resource
    form_class = GlossaryForm
    template_name = "resource_create.html"

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
            return super(ResourceCreateView, self).post(request, *args, **kwargs)


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    context_object_name = "resource"
    template_name = "resource_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ResourceDetailView, self).get_context_data(**kwargs)
        num_of_items = context["resource"].items.all().count()
        context.update(
            {
                "num_of_items": num_of_items,
            }
        )
        return context


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    context_object_name = "resource"
    template_name = "resource_update.html"

    def get_form_class(self):
        if self.object.resource_type == "GLOSSARY":
            return GlossaryForm
        return TranslationUpdateForm

    def form_valid(self, form):
        updated_resource = form.save(commit=False)
        updated_resource.updated_by = self.request.user
        updated_resource.save()
        return HttpResponseRedirect(updated_resource.get_absolute_url())


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    context_object_name = "resource"
    success_url = reverse_lazy("home")
    template_name = "resource_delete.html"
