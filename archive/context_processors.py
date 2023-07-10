from itertools import chain

from .models import Glossary, Translation
from django.db.models.functions import Lower


def resources_processor(request):
    """
    Provides a list of resources to populate the resource drop-down menu
    in the search form included in the navigation bar on each page.
    """
    glossaries = Glossary.objects.all().order_by(Lower("title"))
    translations = Translation.objects.all().order_by(Lower("title"))
    resources = list(chain(glossaries, translations))
    data = {
        "glossaries": glossaries,
        "translations": translations,
        "resources": resources,
    }
    return data
