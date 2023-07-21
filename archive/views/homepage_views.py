from itertools import chain

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Entry, Glossary, Segment, Translation, Resource, Item


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """
        Create list of all resources ordered by creation date.
        Also get the quantity of each type of resource.
        """

        """
        # Could remove the following and just use the list of resources
        # provided by the context processor. However, the order is different.
        glossaries = Glossary.objects.all()
        translations = Translation.objects.all()
        resources_list = sorted(
            chain(glossaries, translations),
            key=lambda item: item.created_on,
            reverse=True,
        )
        """

        resources_list = Resource.objects.all()

        # num_of_glossaries = len(glossaries)
        num_of_glossaries = Resource.objects.filter(resource_type="GLOSSARY").count()
        # num_of_translations = len(translations)
        num_of_translations = Resource.objects.filter(resource_type="TRANSLATION").count()
        # num_of_resources = len(resources_list)
        num_of_resources = Resource.objects.all().count()

        # num_of_gloss_entries = Entry.objects.all().count()
        num_of_gloss_entries = Item.objects.filter(resource__resource_type="GLOSSARY").count()
        # num_of_trans_segments = Segment.objects.all().count()
        num_of_trans_segments = Item.objects.filter(resource__resource_type="TRANSLATION").count()
        # num_of_all_entries = num_of_gloss_entries + num_of_trans_segments
        num_of_all_entries = Item.objects.all().count()

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

    # glossaries = Glossary.objects.all()
    # translations = Translation.objects.all()
    # resources = chain(glossaries, translations)
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
