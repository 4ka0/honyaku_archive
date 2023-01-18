from django.test import TestCase
from django.contrib.auth import get_user_model

from ...models import Translation

from freezegun import freeze_time


class TranslationModelTests(TestCase):

    @classmethod
    @freeze_time("2022-11-11")
    def setUpTestData(cls):
        User = get_user_model()
        cls.testuser = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testuser123",
        )
        cls.translation_obj = Translation.objects.create(
            translation_file=None,
            job_number="ABC123",
            field="Chemical",
            client="BASF",
            translator="Lee",
            notes="Some notes.",
            type="翻訳",
        )

    # Check field labels are correct when object created

    def test_translation_file_label(self):
        field_label = self.translation_obj._meta.get_field("translation_file").verbose_name
        self.assertEqual(field_label, "translation file")
        self.assertNotEqual(field_label, "translation_file")
        self.assertNotEqual(field_label, "")

    def test_job_number_label(self):
        field_label = self.translation_obj._meta.get_field("job_number").verbose_name
        self.assertEqual(field_label, "job number")
        self.assertNotEqual(field_label, "job_number")
        self.assertNotEqual(field_label, "")

    def test_field_label(self):
        field_label = self.translation_obj._meta.get_field("field").verbose_name
        self.assertEqual(field_label, "field")
        self.assertNotEqual(field_label, "")

    def test_client_label(self):
        field_label = self.translation_obj._meta.get_field("client").verbose_name
        self.assertEqual(field_label, "client")
        self.assertNotEqual(field_label, "")

    def test_translator_label(self):
        field_label = self.translation_obj._meta.get_field("translator").verbose_name
        self.assertEqual(field_label, "translator")
        self.assertNotEqual(field_label, "")

    def test_notes_label(self):
        field_label = self.translation_obj._meta.get_field("notes").verbose_name
        self.assertEqual(field_label, "notes")
        self.assertNotEqual(field_label, "")

    def test_created_on_label(self):
        field_label = self.translation_obj._meta.get_field("created_on").verbose_name
        self.assertEqual(field_label, "created on")
        self.assertNotEqual(field_label, "created_on")
        self.assertNotEqual(field_label, "")

    def test_created_by_label(self):
        field_label = self.translation_obj._meta.get_field("created_by").verbose_name
        self.assertEqual(field_label, "created by")
        self.assertNotEqual(field_label, "created_by")
        self.assertNotEqual(field_label, "")

    def test_type_label(self):
        field_label = self.translation_obj._meta.get_field("type").verbose_name
        self.assertEqual(field_label, "type")
        self.assertNotEqual(field_label, "")
