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
            title="ABC123",
            field="Chemical",
            client="ABC Co., Ltd.",
            translator="Lee",
            notes="Some notes.",
            type="翻訳",
            created_by=cls.testuser,
        )

    # Check field labels are correct when object created

    def test_translation_file_label(self):
        field_label = self.translation_obj._meta.get_field(
            "translation_file"
        ).verbose_name
        self.assertEqual(field_label, "translation file")
        self.assertNotEqual(field_label, "translation_file")
        self.assertNotEqual(field_label, "")

    def test_title_label(self):
        field_label = self.translation_obj._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")
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

    def test_translation_file_field_when_created(self):
        self.assertEqual(self.translation_obj.translation_file, None)

    def test_title_field_when_created(self):
        self.assertEqual(self.translation_obj.title, "ABC123")
        self.assertNotEqual(self.translation_obj.title, "")

    def test_field_field_when_created(self):
        self.assertEqual(self.translation_obj.field, "Chemical")
        self.assertNotEqual(self.translation_obj.field, "")

    def test_client_field_when_created(self):
        self.assertEqual(self.translation_obj.client, "ABC Co., Ltd.")
        self.assertNotEqual(self.translation_obj.client, "")

    def test_translator_field_when_created(self):
        self.assertEqual(self.translation_obj.translator, "Lee")
        self.assertNotEqual(self.translation_obj.translator, "")

    def test_notes_field_when_created(self):
        self.assertEqual(self.translation_obj.notes, "Some notes.")
        self.assertNotEqual(self.translation_obj.notes, "")

    def test_type_field_when_created(self):
        self.assertEqual(self.translation_obj.type, "翻訳")
        self.assertNotEqual(self.translation_obj.type, "")

    def test_created_on_field_when_created(self):
        self.assertEqual(
            "2022-11-11 00:00:00+00:00", str(self.translation_obj.created_on)
        )
        self.assertNotEqual("", str(self.translation_obj.created_on))

    def test__created_by_field_when_created(self):
        self.assertEqual(self.translation_obj.created_by, self.testuser)

    # Check field values are correct when updated

    def test_title_field_when_updated(self):
        self.translation_obj.title = "ZZZ369"
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.title, "ZZZ369")
        self.assertNotEqual(self.translation_obj.title, "ABC123")

    def test_field_field_when_updated(self):
        self.translation_obj.field = "Mechanical"
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.field, "Mechanical")
        self.assertNotEqual(self.translation_obj.field, "Chemical")

    def test_client_field_when_updated(self):
        self.translation_obj.client = "IBM"
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.client, "IBM")
        self.assertNotEqual(self.translation_obj.client, "ABC Co., Ltd.")

    def test_translator_field_when_updated(self):
        self.translation_obj.translator = "Hashimoto"
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.translator, "Hashimoto")
        self.assertNotEqual(self.translation_obj.translator, "Lee")

    def test_notes_field_when_updated(self):
        self.translation_obj.notes = "A new note."
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.notes, "A new note.")
        self.assertNotEqual(self.translation_obj.notes, "Some notes.")

    def test_type_field_when_updated(self):
        self.translation_obj.type = "A new note."
        self.translation_obj.save()
        self.assertEqual(self.translation_obj.type, "A new note.")
        self.assertNotEqual(self.translation_obj.type, "Some notes.")

    # Check field properties

    def test_translation_file_can_be_null(self):
        null_bool = self.translation_obj._meta.get_field("translation_file").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_title_max_length(self):
        max_length = self.translation_obj._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_field_max_length(self):
        max_length = self.translation_obj._meta.get_field("field").max_length
        self.assertEqual(max_length, 100)

    def test_client_max_length(self):
        max_length = self.translation_obj._meta.get_field("client").max_length
        self.assertEqual(max_length, 100)

    def test_translator_max_length(self):
        max_length = self.translation_obj._meta.get_field("translator").max_length
        self.assertEqual(max_length, 100)

    def test_type_max_length(self):
        max_length = self.translation_obj._meta.get_field("type").max_length
        self.assertEqual(max_length, 10)

    def test_notes_blank_is_true(self):
        blank_bool = self.translation_obj._meta.get_field("notes").blank
        self.assertEqual(blank_bool, True)
        self.assertNotEqual(blank_bool, False)

    def test_created_on_auto_now_add_is_true(self):
        auto_now_add_bool = self.translation_obj._meta.get_field(
            "created_on"
        ).auto_now_add
        self.assertEqual(auto_now_add_bool, True)
        self.assertNotEqual(auto_now_add_bool, False)

    def test_created_by_related_name(self):
        user_created_translations = self.testuser.created_translations.all()
        self.assertEqual(len(user_created_translations), 1)
        self.assertEqual(user_created_translations[0].title, "ABC123")
        self.assertEqual(user_created_translations[0].client, "ABC Co., Ltd.")

    def test_created_by_foreign_key_set_to_null_when_user_is_deleted(self):
        User = get_user_model()
        testuser_2 = User.objects.create_user(
            username="testuser_2",
            email="test_user_2@email.com",
            password="testuser1234",
        )
        new_translation_obj = Translation.objects.create(
            translation_file=None,
            title="ABC123",
            field="Chemical",
            client="ABC Co., Ltd.",
            translator="Lee",
            notes="Some notes.",
            type="翻訳",
            created_by=testuser_2,
        )
        self.assertEqual(new_translation_obj.created_by, testuser_2)
        testuser_2.delete()
        new_translation_obj.refresh_from_db()
        self.assertEqual(new_translation_obj.created_by, None)

    # Check meta fields

    def test_verbose_name(self):
        verbose_name = self.translation_obj._meta.verbose_name
        self.assertEqual(verbose_name, "translation")
        self.assertNotEqual(verbose_name, "")

    def test_verbose_name_plural(self):
        verbose_name_plural = self.translation_obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "translations")
        self.assertNotEqual(verbose_name_plural, "")
        self.assertNotEqual(verbose_name_plural, "translation")

    # Check class methods

    def test_str_representation(self):
        self.assertEqual(str(self.translation_obj), "ABC123")
        self.assertNotEqual(str(self.translation_obj), "")

    def test_absolute_url(self):
        self.assertEqual(self.translation_obj.get_absolute_url(), "/translation/1/")
        self.assertNotEqual(self.translation_obj.get_absolute_url(), "")
