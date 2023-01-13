from django.test import TestCase
from django.contrib.auth import get_user_model

from ...models import Glossary, Entry

from freezegun import freeze_time


class EntryModelTests(TestCase):

    @classmethod
    @freeze_time("2022-11-11")
    def setUpTestData(cls):
        User = get_user_model()
        cls.testuser = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testuser123",
        )
        cls.glossary_obj = Glossary.objects.create(
            title="Test Glossary",
            notes="Test note.",
            type="用語集",
            created_by=cls.testuser,
            updated_by=cls.testuser,
        )
        cls.entry_obj = Entry.objects.create(
            glossary=cls.glossary_obj,
            source="テスト",
            target="test",
            notes="Just a test.",
            created_by=cls.testuser,
            updated_by=cls.testuser,
        )
