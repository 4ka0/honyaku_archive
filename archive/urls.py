from django.urls import path

from .views.glossary_upload_view import GlossaryUploadView
from .views.homepage_views import HomePageView, home_table_sort
from .views.item_views import ItemCreateView, ItemDeleteView, ItemUpdateView
from .views.resource_views import (ResourceCreateView, ResourceDeleteView,
                                   ResourceDetailView, ResourceUpdateView)
from .views.search_view import SearchView
from .views.translation_upload_view import TranslationUploadView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("home_table_sort/<filter>/<direction>/", home_table_sort, name="home_table_sort"),

    path("search/", SearchView.as_view(), name="search"),

    path("resource/item/new/", ItemCreateView.as_view(), name="create_item"),
    path("resource/<int:resource>/additem/", ItemCreateView.as_view(), name="create_item"),
    path("resource/item/<int:pk>/edit/", ItemUpdateView.as_view(), name="update_item"),
    path("resource/item/<int:pk>/delete/", ItemDeleteView.as_view(), name="delete_item"),

    path("resource/new/", ResourceCreateView.as_view(), name="create_resource"),
    path("resource/<int:pk>/", ResourceDetailView.as_view(), name="resource_detail"),
    path("resource/<int:pk>/edit/", ResourceUpdateView.as_view(), name="resource_update"),
    path("resource/<int:pk>/delete/", ResourceDeleteView.as_view(), name="resource_delete"),

    path("glossary/upload/", GlossaryUploadView.as_view(), name="glossary_upload"),
    path("translation/upload/", TranslationUploadView.as_view(), name="translation_upload"),
]
