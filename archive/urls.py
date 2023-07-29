from django.urls import path

from .views.glossary_item_views import (GlossaryCreateItemView,
                                        GlossaryDeleteItemView,
                                        GlossaryUpdateItemView)
from .views.glossary_views import (GlossaryAddItemView, GlossaryCreateView,
                                   GlossaryUpdateView, GlossaryUploadView)
from .views.homepage_views import HomePageView, home_table_sort
from .views.resource_views import ResourceDeleteView, ResourceDetailView
from .views.search_views import SearchView
from .views.translation_item_views import TranslationDeleteItemView, TranslationUpdateItemView
from .views.translation_views import TranslationUpdateView, TranslationUploadView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("home_table_sort/<filter>/<direction>/", home_table_sort, name="home_table_sort"),

    path("search/", SearchView.as_view(), name="search"),

    path("resource/<int:pk>/", ResourceDetailView.as_view(), name="resource_detail"),
    path("resource/<int:pk>/delete/", ResourceDeleteView.as_view(), name="resource_delete"),

    path("resource/glossary/new/", GlossaryCreateView.as_view(), name="glossary_create"),
    path("resource/glossary/upload/", GlossaryUploadView.as_view(), name="glossary_upload"),
    path("resource/glossary/<int:pk>/edit/", GlossaryUpdateView.as_view(), name="glossary_update"),

    path("resource/glossary/<int:resource>/add/", GlossaryAddItemView.as_view(),
         name="glossary_add_item"),
    path("resource/glossary/item/new/", GlossaryCreateItemView.as_view(),
         name="glossary_create_item"),
    path("resource/glossary/item/<int:pk>/edit/", GlossaryUpdateItemView.as_view(),
         name="glossary_update_item"),
    path("resource/glossary/item/<int:pk>/delete/", GlossaryDeleteItemView.as_view(),
         name="glossary_delete_item"),

    path("resource/translation/upload/", TranslationUploadView.as_view(),
         name="translation_upload"),
    path("resource/translation/<int:pk>/edit/", TranslationUpdateView.as_view(),
         name="translation_update"),

    path("resource/translation/item/<int:pk>/edit/", TranslationUpdateItemView.as_view(),
         name="translation_update_item"),
    path("resource/translation/item/<int:pk>/delete/", TranslationDeleteItemView.as_view(),
         name="translation_delete_item"),
]
