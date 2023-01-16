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

    # Check field labels are correct when object created

    def test_glossary_label(self):
        field_label = self.entry_obj._meta.get_field("glossary").verbose_name
        self.assertEqual(field_label, "glossary")
        self.assertNotEqual(field_label, "")

    def test_source_label(self):
        field_label = self.entry_obj._meta.get_field("source").verbose_name
        self.assertEqual(field_label, "source")
        self.assertNotEqual(field_label, "")

    def test_target_label(self):
        field_label = self.entry_obj._meta.get_field("target").verbose_name
        self.assertEqual(field_label, "target")
        self.assertNotEqual(field_label, "")

    def test_created_on_label(self):
        field_label = self.entry_obj._meta.get_field("created_on").verbose_name
        self.assertEqual(field_label, "created on")
        self.assertNotEqual(field_label, "created_on")
        self.assertNotEqual(field_label, "")

    def test_created_by_label(self):
        field_label = self.entry_obj._meta.get_field("created_by").verbose_name
        self.assertEqual(field_label, "created by")
        self.assertNotEqual(field_label, "created_by")
        self.assertNotEqual(field_label, "")

    def test_updated_on_label(self):
        field_label = self.entry_obj._meta.get_field("updated_on").verbose_name
        self.assertEqual(field_label, "updated on")
        self.assertNotEqual(field_label, "updated_on")
        self.assertNotEqual(field_label, "")

    def test_updated_by_label(self):
        field_label = self.entry_obj._meta.get_field("updated_by").verbose_name
        self.assertEqual(field_label, "updated by")
        self.assertNotEqual(field_label, "updated_by")
        self.assertNotEqual(field_label, "")

    # Check field values are correct when object created

    def test_entry_glossary_field_when_created(self):
        self.assertEqual(self.entry_obj.glossary, self.glossary_obj)
        self.assertNotEqual(self.entry_obj.glossary, None)

    def test_entry_source_field_when_created(self):
        self.assertEqual(self.entry_obj.source, "テスト")
        self.assertNotEqual(self.entry_obj.source, "")

    def test_entry_target_field_when_created(self):
        self.assertEqual(self.entry_obj.target, "test")
        self.assertNotEqual(self.entry_obj.target, "")

    def test_entry_notes_field_when_created(self):
        self.assertEqual(self.entry_obj.notes, "Just a test.")
        self.assertNotEqual(self.entry_obj.notes, "")

    def test_entry_created_by_field_when_created(self):
        self.assertEqual(self.entry_obj.created_by, self.testuser)

    def test_entry_updated_by_field_when_created(self):
        self.assertEqual(self.entry_obj.updated_by, self.testuser)

    def test_entry_created_on_field_when_created(self):
        self.assertEqual("2022-11-11 00:00:00+00:00", str(self.entry_obj.created_on))
        self.assertNotEqual("", str(self.entry_obj.created_on))

    def test_entry_updated_on_field_when_created(self):
        self.assertEqual("2022-11-11 00:00:00+00:00", str(self.entry_obj.updated_on))
        self.assertNotEqual("", str(self.entry_obj.updated_on))

    # Check field values are correct when updated
