from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from ..models import Item, Resource
from ..forms.item_forms import GlossaryItemForm


class GlossaryCreateItemView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = GlossaryItemForm
    template_name = "item_create.html"

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.created_by = self.request.user
        new_item.updated_by = self.request.user

        # If a new resource is to be created for this item.
        new_resource_title = form.cleaned_data.get("new_resource")
        if new_resource_title:
            new_resource = Resource(
                title=new_resource_title,
                resource_type="GLOSSARY",
                created_by=self.request.user,
                updated_by=self.request.user,
            )
            new_resource.save()
            new_item.resource = new_resource

        new_item.save()

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
            return super(GlossaryCreateItemView, self).post(request, *args, **kwargs)


"""
class GlossaryUpdateItemView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = GlossaryItemForm
    template_name = "item_update.html"

    def form_valid(self, form):
        updated_item = form.save(commit=False)
        updated_item.updated_by = self.request.user

        # If a new resource is to be created for the updated item.
        new_resource_title = form.cleaned_data.get("new_resource")
        if new_resource_title:
            new_resource = Resource(
                title=new_resource_title,
                resource_type="GLOSSARY",
                created_by=self.request.user,
                updated_by=self.request.user,
            )
            new_resource.save()
            updated_item.resource = new_resource

        updated_item.save()

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
            return super(GlossaryUpdateItemView, self).post(request, *args, **kwargs)
"""

"""
class GlossaryDeleteItemView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "item_delete.html"

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
            return super(GlossaryDeleteItemView, self).post(request, *args, **kwargs)
"""
