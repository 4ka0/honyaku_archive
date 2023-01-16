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

    def test_entry_glossary_field_when_updated(self):
        new_glossary_obj = Glossary.objects.create(
            title="Test Glossary 1",
            notes="Test note 2.",
            type="用語集",
            created_by=self.testuser,
            updated_by=self.testuser,
        )
        self.entry_obj.glossary = new_glossary_obj
        self.entry_obj.save()
        self.assertEqual(self.entry_obj.glossary, new_glossary_obj)
        self.assertEqual(self.entry_obj.glossary.title, "Test Glossary 1")
        self.assertNotEqual(self.entry_obj.glossary, self.glossary_obj)

    def test_entry_source_field_when_updated(self):
        self.entry_obj.source = "情報"
        self.entry_obj.save()
        self.assertEqual(self.entry_obj.source, "情報")
        self.assertNotEqual(self.entry_obj.source, "テスト")

    def test_entry_target_field_when_updated(self):
        self.entry_obj.target = "information"
        self.entry_obj.save()
        self.assertEqual(self.entry_obj.target, "information")
        self.assertNotEqual(self.entry_obj.target, "test")

    def test_entry_created_by_field_when_updated(self):
        User = get_user_model()
        new_testuser = User.objects.create_user(
            username="new_test_user",
            email="new_test_user@email.com",
            password="testuser1234",
        )
        self.entry_obj.created_by = new_testuser
        self.entry_obj.save()
        self.assertEqual(self.entry_obj.created_by, new_testuser)
        self.assertNotEqual(self.entry_obj.created_by, self.testuser)

    def test_entry_updated_by_field_when_updated(self):
        User = get_user_model()
        new_testuser = User.objects.create_user(
            username="new_test_user",
            email="new_test_user@email.com",
            password="testuser1234",
        )
        self.entry_obj.updated_by = new_testuser
        self.entry_obj.save()
        self.assertEqual(self.entry_obj.updated_by, new_testuser)
        self.assertNotEqual(self.entry_obj.updated_by, self.testuser)

    @freeze_time("2023-01-01")
    def test_object_updated_on_field_when_updated(self):
        self.entry_obj.source = "情報"
        self.entry_obj.save()
        self.assertEqual(str(self.entry_obj.updated_on), "2023-01-01 00:00:00+00:00")
        self.assertNotEqual(str(self.entry_obj.updated_on), "2022-11-11 00:00:00+00:00")
