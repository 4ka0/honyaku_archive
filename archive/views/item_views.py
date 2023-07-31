from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from ..forms.item_forms import GlossaryItemForm, TranslationItemForm, GlossaryAddItemForm
from ..models import Item, Resource


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = "item_create.html"

    def get_form_class(self):
        # If to create Item from scratch
        #    return ItemCreateForm
        # return ItemAddForm
        return GlossaryItemForm

    def get_success_url(self):
        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return previous_url
        return reverse_lazy("home")

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
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(ItemCreateView, self).post(request, *args, **kwargs)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
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


class GlossaryAddItemView(LoginRequiredMixin, CreateView):
    """
    Class to add a new Item object to an existing Resource Object.
    Called from the resource detail page.
    Receives pk of resource object in question and sets this for the
    entry.glossary field.
    """

    model = Item
    form_class = GlossaryAddItemForm
    template_name = "glossary_add_item.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.resource = Resource.objects.get(pk=self.kwargs["resource"])
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
            return super(GlossaryAddItemView, self).post(request, *args, **kwargs)
