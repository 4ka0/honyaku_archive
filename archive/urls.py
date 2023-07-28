from django.urls import path

from .views.homepage_views import (
    HomePageView,
    home_table_sort,
)

from .views.search_views import (
    SearchView,
)

from .views.resource_views import (
    ResourceDetailView,
    ResourceDeleteView,
)

from .views.glossary_item_views import (
    GlossaryItemCreateView,
    GlossaryItemUpdateView,
    GlossaryItemDeleteView,
)

from .views.glossary_views import (
    GlossaryUploadView,
    # GlossaryDetailView,
    GlossaryCreateView,
    # GlossaryDeleteView,
    GlossaryAddItemView,
    # GlossaryAllEntryView,
    GlossaryUpdateView,
)

from .views.translation_item_views import SegmentUpdateView, SegmentDeleteView

from .views.translation_views import (
    # TranslationDetailView,
    TranslationUpdateView,
    TranslationDeleteView,
    TranslationUploadView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("home_table_sort/<filter>/<direction>/", home_table_sort, name="home_table_sort"),

    path("search/", SearchView.as_view(), name="search"),

    # New URLS
    path("resource/<int:pk>/", ResourceDetailView.as_view(), name="resource_detail"),
    path("resource/<int:pk>/delete/", ResourceDeleteView.as_view(), name="resource_delete"),
    path("glossary/<int:resource>/add/", GlossaryAddItemView.as_view(), name="resource_add_item"),

    # Old URLs
    path("glossary/new/", GlossaryCreateView.as_view(), name="glossary_create"),
    path("glossary/upload/", GlossaryUploadView.as_view(), name="glossary_upload"),
    path("glossary/<int:pk>/edit/", GlossaryUpdateView.as_view(), name="glossary_update"),

    path("entry/new/", GlossaryItemCreateView.as_view(), name="entry_create"),
    path("entry/<int:pk>/edit/", GlossaryItemUpdateView.as_view(), name="entry_update"),
    path("entry/<int:pk>/delete/", GlossaryItemDeleteView.as_view(), name="entry_delete"),

    path("translation/upload/", TranslationUploadView.as_view(), name="translation_upload"),
    path("translation/<int:pk>/edit/", TranslationUpdateView.as_view(), name="translation_update"),
    path(
        "translation/<int:pk>/delete/",
        TranslationDeleteView.as_view(),
        name="translation_delete"
    ),

    path("segment/<int:pk>/edit/", SegmentUpdateView.as_view(), name="segment_update"),
    path("segment/<int:pk>/delete/", SegmentDeleteView.as_view(), name="segment_delete"),
]
