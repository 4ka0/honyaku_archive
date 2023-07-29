from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView

from ..models import Item, Resource


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    template_name = "resource_detail.html"
    context_object_name = "resource"

    def get_context_data(self, **kwargs):
        context = super(ResourceDetailView, self).get_context_data(**kwargs)
        num_of_items = context["resource"].items.all().count()
        context.update(
            {
                "num_of_items": num_of_items,
            }
        )
        return context


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = "resource_delete.html"
    context_object_name = "resource"
    success_url = reverse_lazy("home")


class ResourceDeleteItemView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "item_delete.html"
    context_object_name = "item"

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
            return super(ResourceDeleteItemView, self).post(request, *args, **kwargs)
