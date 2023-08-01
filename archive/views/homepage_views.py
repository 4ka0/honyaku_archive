from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Resource, Item


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        resources_list = Resource.objects.all()

        num_of_resources = Resource.objects.all().count()
        num_of_glossaries = Resource.objects.filter(resource_type="GLOSSARY").count()
        num_of_translations = Resource.objects.filter(resource_type="TRANSLATION").count()

        num_of_all_entries = Item.objects.all().count()
        num_of_gloss_entries = Item.objects.filter(resource__resource_type="GLOSSARY").count()
        num_of_trans_segments = Item.objects.filter(resource__resource_type="TRANSLATION").count()

        autofocus_searchbar = True

        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update(
            {
                "resources_list": resources_list,
                "num_of_glossaries": num_of_glossaries,
                "num_of_translations": num_of_translations,
                "num_of_resources": num_of_resources,
                "num_of_gloss_entries": num_of_gloss_entries,
                "num_of_trans_segments": num_of_trans_segments,
                "num_of_all_entries": num_of_all_entries,
                "autofocus_searchbar": autofocus_searchbar,
            }
        )
        return context


def home_table_sort(request, filter, direction):
    """
    View to sort and redisplay the glossaries and translations displayed in the
    table shown on the homepage. Receives HTMX ajax calls from the template.
    """

    resources = Resource.objects.all()

    if direction == "ascend":
        direction = False
    else:
        direction = True

    if filter == "title":
        resources_list = sorted(
            resources, key=lambda item: item.title, reverse=direction
        )
    elif filter == "type":
        resources_list = sorted(
            resources, key=lambda item: item.resource_type, reverse=direction
        )
    else:
        resources_list = sorted(
            resources, key=lambda item: item.created_on, reverse=direction
        )

    return render(request, "_home_table_list.html", {"resources_list": resources_list})
