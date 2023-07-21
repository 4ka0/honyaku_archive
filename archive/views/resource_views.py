from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Resource


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    template_name = "resource_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ResourceDetailView, self).get_context_data(**kwargs)
        num_of_entries = context["resource"].items.all().count()
        context.update(
            {
                "num_of_entries": num_of_entries,
            }
        )
        return context
