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
            created_by=cls.testuser,
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

    # Check field values are correct when object created

    def test_translation_translation_file_field_when_created(self):
        self.assertEqual(self.translation_obj.translation_file, None)

    def test_translation_job_number_field_when_created(self):
        self.assertEqual(self.translation_obj.job_number, "ABC123")
        self.assertNotEqual(self.translation_obj.job_number, "")

    def test_translation_field_field_when_created(self):
        self.assertEqual(self.translation_obj.field, "Chemical")
        self.assertNotEqual(self.translation_obj.field, "")

    def test_translation_client_field_when_created(self):
        self.assertEqual(self.translation_obj.client, "BASF")
        self.assertNotEqual(self.translation_obj.client, "")

    def test_translation_translator_field_when_created(self):
        self.assertEqual(self.translation_obj.translator, "Lee")
        self.assertNotEqual(self.translation_obj.translator, "")

    def test_translation_notes_field_when_created(self):
        self.assertEqual(self.translation_obj.notes, "Some notes.")
        self.assertNotEqual(self.translation_obj.notes, "")

    def test_translation_type_field_when_created(self):
        self.assertEqual(self.translation_obj.type, "翻訳")
        self.assertNotEqual(self.translation_obj.type, "")

    def test_translation_created_on_field_when_created(self):
        self.assertEqual("2022-11-11 00:00:00+00:00", str(self.translation_obj.created_on))
        self.assertNotEqual("", str(self.translation_obj.created_on))

    def test_translation__created_by_field_when_created(self):
        self.assertEqual(self.translation_obj.created_by, self.testuser)

    # Check field values are correct when updated

    def test_translation_job_number_field_when_updated(self):
        self.translation_obj.job_number = "ZZZ369"
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.job_number, "ZZZ369")
        self.assertNotEqual(self.translation_obj.job_number, "ABC123")

    def test_translation_field_field_when_updated(self):
        self.translation_obj.field = "Mechanical"
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.field, "Mechanical")
        self.assertNotEqual(self.translation_obj.field, "Chemical")

    def test_translation_client_field_when_updated(self):
        self.translation_obj.client = "IBM"
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.client, "IBM")
        self.assertNotEqual(self.translation_obj.client, "BASF")

    def test_translation_translator_field_when_updated(self):
        self.translation_obj.translator = "Hashimoto"
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.translator, "Hashimoto")
        self.assertNotEqual(self.translation_obj.translator, "Lee")

    def test_translation_notes_field_when_updated(self):
        self.translation_obj.notes = "A new note."
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.notes, "A new note.")
        self.assertNotEqual(self.translation_obj.notes, "Some notes.")

    def test_translation_type_field_when_updated(self):
        self.translation_obj.type = "A new note."
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.type, "A new note.")
        self.assertNotEqual(self.translation_obj.type, "Some notes.")

    # Check field properties
