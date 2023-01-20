from django.test import TestCase
from ...forms import EntryCreateForm

# from freezegun import freeze_time


class TestEntryCreateForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        form = EntryCreateForm()

    # Test fields
    # Test labels
    # Test help text
    # Test form methods created yourself
