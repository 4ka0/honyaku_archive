from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView

from ..models import Resource


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
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


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = "resource_delete.html"
    success_url = reverse_lazy("home")
