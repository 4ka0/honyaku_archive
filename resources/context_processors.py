from itertools import chain

from .models import Glossary, Translation
from django.db.models.functions import Lower


def resources_processor(request):
    glossaries = Glossary.objects.all().order_by(Lower("title"))
    translations = Translation.objects.all().order_by(Lower("job_number"))
    resources = list(chain(glossaries, translations))
    return {'resources': resources}
