from itertools import chain

from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Length

from ..models import Entry, Segment


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

        raw_query = self.request.GET.get("query")

        # Check if query is surrounded with double quotes.
        # If surrounded, remove only the quote symbols.
        #    (I.e. leave whitespace directly inside quote symbols.)
        # If not surrounded, strip any surrounding whitespace.
        if raw_query.startswith('"') and raw_query.endswith('"'):
            query = raw_query[1:-1]
        else:
            query = raw_query.strip()

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
