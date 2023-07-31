from django.urls import path

from .views.glossary_views import (GlossaryCreateView,
                                   GlossaryUpdateView, GlossaryUploadView)
from .views.homepage_views import HomePageView, home_table_sort
from .views.item_views import ItemCreateView, ItemDeleteView, ItemUpdateView, GlossaryAddItemView
from .views.resource_views import ResourceDeleteView, ResourceDetailView
from .views.search_views import SearchView
from .views.translation_views import TranslationUpdateView, TranslationUploadView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("home_table_sort/<filter>/<direction>/", home_table_sort, name="home_table_sort"),

    path("search/", SearchView.as_view(), name="search"),

    path("item/<int:pk>/edit/", ItemUpdateView.as_view(), name="update_item"),
    path("item/<int:pk>/delete/", ItemDeleteView.as_view(), name="delete_item"),

    # Create single ItemCreateView view for the below two?
    path("item/new/", ItemCreateView.as_view(), name="create_item"),
    path("glossary/<int:resource>/add/", GlossaryAddItemView.as_view(), name="glossary_add_item"),

    path("resource/<int:pk>/", ResourceDetailView.as_view(), name="resource_detail"),
    path("resource/<int:pk>/delete/", ResourceDeleteView.as_view(), name="resource_delete"),

    path("resource/glossary/new/", GlossaryCreateView.as_view(), name="glossary_create"),
    path("resource/glossary/upload/", GlossaryUploadView.as_view(), name="glossary_upload"),
    path("resource/glossary/<int:pk>/edit/", GlossaryUpdateView.as_view(), name="glossary_update"),

    path("resource/translation/upload/", TranslationUploadView.as_view(),
         name="translation_upload"),
    path("resource/translation/<int:pk>/edit/", TranslationUpdateView.as_view(),
         name="translation_update"),

]
