from itertools import chain

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Length

from ..models import (
    Entry, Glossary, Segment, Translation
)


class HomePageView(LoginRequiredMixin, TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """
        Create list of all resources ordered by creation date.
        Also get the quantity of each type of resource.
        """

        # Could remove the following and just use the list of resources
        # provided by the context processor. However, the order is different.
        glossaries = Glossary.objects.all()
        translations = Translation.objects.all()
        resources_table_list = sorted(
            chain(glossaries, translations),
            key=lambda item: item.created_on,
            reverse=True
        )

        num_of_glossaries = len(glossaries)
        num_of_translations = len(translations)
        num_of_resources = len(resources_table_list)

        num_of_gloss_entries = Entry.objects.all().count()
        num_of_trans_segments = Segment.objects.all().count()
        num_of_all_entries = num_of_gloss_entries + num_of_trans_segments

        autofocus_searchbar = True

        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            "resources_table_list": resources_table_list,
            "num_of_glossaries": num_of_glossaries,
            "num_of_translations": num_of_translations,
            "num_of_resources": num_of_resources,
            "num_of_gloss_entries": num_of_gloss_entries,
            "num_of_trans_segments": num_of_trans_segments,
            "num_of_all_entries": num_of_all_entries,
            "autofocus_searchbar": autofocus_searchbar,
        })
        return context


def home_table_sort(request, filter, direction):
    glossaries = Glossary.objects.all()
    translations = Translation.objects.all()

    if filter == "title":
        if direction == "ascend":
            resources_table_list = sorted(
                chain(glossaries, translations),
                key=lambda item: item.title,
                reverse=False
            )
        else:
            resources_table_list = sorted(
                chain(glossaries, translations),
                key=lambda item: item.title,
                reverse=True
            )

    elif filter == "type":
        if direction == "ascend":
            resources_table_list = sorted(
                chain(glossaries, translations),
                key=lambda item: item.type,
                reverse=False
            )
        else:
            resources_table_list = sorted(
                chain(glossaries, translations),
                key=lambda item: item.type,
                reverse=True
            )

    else:
        if direction == "ascend":
            resources_table_list = sorted(
                chain(glossaries, translations),
                key=lambda item: item.created_on,
                reverse=False
            )
        else:
            resources_table_list = sorted(
                chain(glossaries, translations),
                key=lambda item: item.created_on,
                reverse=True
            )

    return render(request, '_home_table_list.html', {'resources_table_list': resources_table_list})


class SearchView(LoginRequiredMixin, ListView):
    """
    View to search glossary and translation resources for entries containing
    a query string.
    """

    template_name = "search_results.html"

    def get_queryset(self):
        """
        Overridden to find Entry and Segment objects containing the query.
        """

        query = self.request.GET.get("query").strip()
        resource = self.request.GET.get("resource")

        # Search all resources (glossary entries and translation segments)
        if resource == "すべてのリソース":
            entry_queryset = Entry.objects.filter(
                Q(source__icontains=query) | Q(target__icontains=query)
            ).order_by(Length('source'))
            segment_queryset = Segment.objects.filter(
                Q(source__icontains=query) | Q(target__icontains=query)
            ).order_by(Length('source'))
            queryset = list(chain(entry_queryset, segment_queryset))

        # Search all glossary entries
        elif resource == "すべての用語集":
            queryset = Entry.objects.filter(
                Q(source__icontains=query) | Q(target__icontains=query)
            ).order_by(Length('source'))

        # Search all translation segments
        elif resource == "すべての翻訳":
            queryset = Segment.objects.filter(
                Q(source__icontains=query) | Q(target__icontains=query)
            ).order_by(Length('source'))

        # Search specific resource
        else:
            entry_queryset = Entry.objects.filter(
                Q(glossary__title=resource),
                Q(source__icontains=query) | Q(target__icontains=query)
            ).order_by(Length('source'))
            segment_queryset = Segment.objects.filter(
                Q(translation__title=resource),
                Q(source__icontains=query) | Q(target__icontains=query)
            ).order_by(Length('source'))
            queryset = list(chain(entry_queryset, segment_queryset))

        return queryset

    def get_context_data(self, **kwargs):
        """
        Overridden to provide data used for the results message.
        """

        context = super(SearchView, self).get_context_data(**kwargs)

        query = self.request.GET.get("query").strip()
        target_resource = self.request.GET.get("resource")

        hits = len(self.get_queryset())
        context.update({
            "query": query,
            "target_resource": target_resource,
            "hits": hits,
        })

        return context
