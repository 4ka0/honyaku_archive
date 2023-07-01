from django.urls import path

from .views.main_views import HomePageView, SearchView

from .views.entry_views import (
    EntryCreateView,
    EntryDetailView,
    EntryUpdateView,
    EntryDeleteView,
)

from .views.glossary_views import (
    GlossaryUploadView,
    GlossaryDetailView,
    GlossaryCreateView,
    GlossaryDeleteView,
    GlossaryAddEntryView,
    GlossaryAllEntryView,
    GlossaryUpdateView,
)

from .views.segment_views import SegmentUpdateView, SegmentDeleteView

from .views.translation_views import (
    TranslationDetailView,
    TranslationUpdateView,
    TranslationDeleteView,
    TranslationUploadView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),

    path("search/", SearchView.as_view(), name="search"),

    path("entry/new/", EntryCreateView.as_view(), name="entry_create"),
    path("entry/<int:pk>/", EntryDetailView.as_view(), name="entry_detail"),
    path("entry/<int:pk>/edit/", EntryUpdateView.as_view(), name="entry_update"),
    path("entry/<int:pk>/delete/", EntryDeleteView.as_view(), name="entry_delete"),

    path("glossary/new/", GlossaryCreateView.as_view(), name="glossary_create"),
    path("glossary/upload/", GlossaryUploadView.as_view(), name="glossary_upload"),
    path("glossary/<int:pk>/", GlossaryDetailView.as_view(), name="glossary_detail"),
    path("glossary/<int:pk>/delete/", GlossaryDeleteView.as_view(), name="glossary_delete"),
    path("glossary/<int:glossary>/add/", GlossaryAddEntryView.as_view(), name="glossary_add_entry"),
    path("glossary/<int:pk>/all/", GlossaryAllEntryView.as_view(), name="glossary_all_entries"),
    path("glossary/<int:pk>/edit/", GlossaryUpdateView.as_view(), name="glossary_update"),
    # path("glossary/export/", GlossaryExportView.as_view(), name="glossary_export"),

    path("segment/<int:pk>/edit/", SegmentUpdateView.as_view(), name="segment_update"),
    path("segment/<int:pk>/delete/", SegmentDeleteView.as_view(), name="segment_delete"),

    path("translation/upload/", TranslationUploadView.as_view(), name="translation_upload"),
    path("translation/<int:pk>/", TranslationDetailView.as_view(), name="translation_detail"),
    path("translation/<int:pk>/edit/", TranslationUpdateView.as_view(), name="translation_update"),
    path(
        "translation/<int:pk>/delete/",
        TranslationDeleteView.as_view(),
        name="translation_delete"
    ),
]
