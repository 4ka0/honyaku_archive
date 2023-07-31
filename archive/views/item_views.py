from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from ..forms.glossary_item_forms import GlossaryItemForm, TranslationItemForm
from ..models import Item


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
