from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Glossary, Entry

from freezegun import freeze_time


class ResourcesTagTests(TestCase):

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
        Entry.objects.create(
            glossary=cls.test_glossary,
            source="鍵情報",
            target="key information",
            notes="Test note.",
        )

    def setUp(self):
        self.client.force_login(self.test_user)
        self.url = reverse('search_results')

    def test_simple_case_success(self):
        response = self.client.get(self.url, {'query': 'Information', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">Information</span>')

    def test_simple_case_failure(self):
        response = self.client.get(self.url, {'query': 'Information', 'resource': 'Test Glossary'})
        self.assertNotContains(response, '<span class="highlight_query">&lt;Information processing device &amp; display device&gt;</span>')

    def test_highlight_not_included_in_output_if_query_not_found(self):
        response = self.client.get(self.url, {'query': 'window', 'resource': 'Test Glossary'})
        self.assertNotContains(response, '<span class="highlight_query">window</span>')

    def test_display_of_opening_angle_bracket(self):
        response = self.client.get(self.url, {'query': '<Info', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">&lt;Info</span>')

    def test_display_of_closing_angle_bracket(self):
        response = self.client.get(self.url, {'query': 'device>', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">device&gt;</span>')

    def test_display_of_ampersand(self):
        response = self.client.get(self.url, {'query': 'device & display', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">device &amp; display</span>')

    def test_highlight_is_applied_in_case_insensitive_manner_lowercase(self):
        response = self.client.get(self.url, {'query': 'information', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">Information</span>')

    def test_highlight_is_applied_in_case_insensitive_manner_uppercase(self):
        response = self.client.get(self.url, {'query': 'INFORMATION', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">Information</span>')

    def test_highlight_is_applied_in_case_insensitive_manner_mixed_case(self):
        response = self.client.get(self.url, {'query': 'INforMAtiON', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">Information</span>')

    def test_highlight_is_applied_in_japanese_source_text(self):
        response = self.client.get(self.url, {'query': '情報', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">情報</span>処理装置')

    def test_highlight_is_applied_multiple_times_when_there_are_multiple_results(self):
        response = self.client.get(self.url, {'query': 'information', 'resource': 'Test Glossary'})
        self.assertContains(response, '<span class="highlight_query">Information</span> processing device')
        self.assertContains(response, 'key <span class="highlight_query">information</span>')
