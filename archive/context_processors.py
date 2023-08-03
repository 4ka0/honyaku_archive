from django.db.models.functions import Lower

from .models import Resource


def resources_processor(request):
    """
    Provides resources to populate the resource drop-down menu in the search
    form included in the navigation bar on each page.
    """
    glossaries = Resource.objects.filter(resource_type="GLOSSARY").order_by(Lower("title"))
    translations = Resource.objects.filter(resource_type="TRANSLATION").order_by(Lower("title"))
    data = {
        "glossaries": glossaries,
        "translations": translations,
    }
    return data
