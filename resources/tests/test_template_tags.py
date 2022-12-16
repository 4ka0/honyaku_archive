from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Glossary, Entry

from freezegun import freeze_time


class ResourcesTagTests(TestCase):
    """
    Create Glossary object
    Create Entry object containing all chars that might be mistaken for html
    or regex chars.
    Each method searches for specific char.
    Check html output is as expected.
    """

    @classmethod
    @freeze_time("2022-12-01")
    def setUpTestData(cls):

        User = get_user_model()
        cls.test_user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testuser1234",
        )

        cls.test_glossary = Glossary.objects.create(
            title="Test Glossary",
            notes="Test note.",
            type="用語集",
            created_by=cls.test_user,
            updated_by=cls.test_user,
        )

        Entry.objects.create(
            glossary=cls.test_glossary,
            source="情報処理装置",
            target="<Information processing device & display device>",
            notes="Test note.",
        )

    def setUp(self):
        self.client.force_login(self.test_user)

    def test_display_of_opening_angle_bracket(self):
        url = reverse('search_results')
        response = self.client.get(url, {'query': '<', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">&lt;</span>')

    def test_display_of_closing_angle_bracket(self):
        pass

    def test_display_of_ampersand(self):
        pass
