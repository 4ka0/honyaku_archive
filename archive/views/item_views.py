from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from ..forms.item_forms import GlossaryItemForm, TranslationItemForm, GlossaryAddItemForm
from ..models import Item, Resource


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    Class to create a new Item or add a new Item to a Resource.
    Either called from the navigation bar (in which case a new Item is to be
    created), or called from the resource detail page (in which case a new Item
    is to be added to the Resource object in question).
    """
    model = Item
    template_name = "item_create.html"

    def get_form_class(self):
        """
        If this view is called from the resource detail page, the pk of the
        Resource object in question is passed as the keyword argument "resource".
        If called from the navigation bar, "resource" should not be present.
        """
        if "resource" in self.kwargs:
            return GlossaryAddItemForm
        return GlossaryItemForm

    def get_success_url(self, new_item):
        """
        Redirect to the detail page of the Resource object to which the new
        Item object belongs. Otherwise redirect to the previous URL, or simply
        redirect to home.
        """
        if new_item.resource:
            resource = new_item.resource
            return resource.get_absolute_url()
        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return previous_url
        return reverse_lazy("home")

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.created_by = self.request.user
        new_item.updated_by = self.request.user

        # If a new resource is to be created for the new item.
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

        # If the resource to be associated with the new item has been passed as
        # a parameter in the URL.
        if "resource" in self.kwargs:
            resource_pk = self.kwargs["resource"]
            new_item.resource = Resource.objects.get(pk=resource_pk)

        new_item.save()
        return HttpResponseRedirect(self.get_success_url(new_item))

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(ItemCreateView, self).post(request, *args, **kwargs)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    Class to update an existing Item.
    Different forms are used depending on whether the Item belongs to a
    glossary or a translation.
    """
    model = Item
    template_name = "item_update.html"

    def get_form_class(self):
        if self.object.resource.resource_type == "GLOSSARY":
            return GlossaryItemForm
        return TranslationItemForm

    def get_success_url(self):
        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return previous_url
        return reverse_lazy("home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    context_object_name = "item"
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
            return super(ItemDeleteView, self).post(request, *args, **kwargs)
