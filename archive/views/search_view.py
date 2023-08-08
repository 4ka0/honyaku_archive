from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Length

from ..models import Item


class SearchView(LoginRequiredMixin, ListView):
    """
    View to search for Item objects containing a query string.
    """
    template_name = "search_results.html"

    def get_queryset(self):
        resource = self.request.GET.get("resource")
        raw_query = self.request.GET.get("query")

        # Check if query is surrounded with double quotes.
        # If surrounded, remove only the quote symbols.
        #    (I.e. leave whitespace directly inside quote symbols.)
        # If not surrounded, strip any surrounding whitespace.
        if raw_query.startswith('"') and raw_query.endswith('"'):
            query = raw_query[1:-1]
        else:
            query = raw_query.strip()

        # Search all resources
        if resource == "すべてのリソース":
            queryset = (
                Item.objects
                .filter(Q(source__icontains=query) | Q(target__icontains=query) | Q(notes__icontains=query))
                .order_by(Length("source"))
            )

        # Search all glossaries
        elif resource == "すべての用語集":
            queryset = (
                Item.objects
                .filter(resource__resource_type="GLOSSARY")
                .filter(Q(source__icontains=query) | Q(target__icontains=query) | Q(notes__icontains=query))
                .order_by(Length("source"))
            )

        # Search all translations
        elif resource == "すべての翻訳":
            queryset = (
                Item.objects
                .filter(resource__resource_type="TRANSLATION")
                .filter(Q(source__icontains=query) | Q(target__icontains=query) | Q(notes__icontains=query))
                .order_by(Length("source"))
            )

        # Search specific resource
        else:
            queryset = (
                Item.objects
                .filter(
                    Q(resource__title=resource),
                    Q(source__icontains=query) | Q(target__icontains=query) | Q(notes__icontains=query),
                )
                .order_by(Length("source"))
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Overridden to provide data used for the results message.
        """
        context = super(SearchView, self).get_context_data(**kwargs)

        query = self.request.GET.get("query").strip()
        target_resource = self.request.GET.get("resource")
        hits = len(self.get_queryset())
        
        context.update(
            {
                "query": query,
                "target_resource": target_resource,
                "hits": hits,
            }
        )

        return context
