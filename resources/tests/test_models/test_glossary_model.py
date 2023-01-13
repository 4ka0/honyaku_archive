from django.test import TestCase
from django.contrib.auth import get_user_model

from ...models import Glossary

from freezegun import freeze_time


class GlossaryModelTests(TestCase):

    @classmethod
    @freeze_time("2022-11-11")
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testuser123",
        )
        Glossary.objects.create(
            title="test glossary",
            notes="Test note.",
            type="用語集",
            created_by=cls.user,
            updated_by=cls.user,
        )

    # Check field labels created correctly

    def test_glossary_file_label(self):
        glossary_obj = Glossary.objects.get(id=1)
        field_label = glossary_obj._meta.get_field("glossary_file").verbose_name
        self.assertEqual(field_label, "glossary file")
        self.assertNotEqual(field_label, "glossary_file")
        self.assertNotEqual(field_label, "")

    def test_title_label(self):
        glossary_obj = Glossary.objects.get(id=1)
        field_label = glossary_obj._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")
        self.assertNotEqual(field_label, "")

    def test_created_by_label(self):
        glossary_obj = Glossary.objects.get(id=1)
        field_label = glossary_obj._meta.get_field("created_by").verbose_name
        self.assertEqual(field_label, "created by")
        self.assertNotEqual(field_label, "created_by")
        self.assertNotEqual(field_label, "")

    def test_updated_by_label(self):
        glossary_obj = Glossary.objects.get(id=1)
        field_label = glossary_obj._meta.get_field("updated_by").verbose_name
        self.assertEqual(field_label, "updated by")
        self.assertNotEqual(field_label, "updated_by")
        self.assertNotEqual(field_label, "")

    def test_notes_label(self):
        glossary_obj = Glossary.objects.get(id=1)
        field_label = glossary_obj._meta.get_field("notes").verbose_name
        self.assertEqual(field_label, "notes")
        self.assertNotEqual(field_label, "")

    def test_type_label(self):
        glossary_obj = Glossary.objects.get(id=1)
        field_label = glossary_obj._meta.get_field("type").verbose_name
        self.assertEqual(field_label, "type")
        self.assertNotEqual(field_label, "")

    # Check whether object is created correctly

    def test_glossary_title_field_when_created(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual(glossary_obj.title, "test glossary")
        self.assertNotEqual(glossary_obj.title, "")

    def test_glossary_notes_field_when_created(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual(glossary_obj.notes, "Test note.")
        self.assertNotEqual(glossary_obj.notes, "")

    def test_glossary_type_field_when_created(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual(glossary_obj.type, "用語集")
        self.assertNotEqual(glossary_obj.type, "")

    def test_glossary_created_by_field_when_created(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual(glossary_obj.created_by, self.user)

    def test_glossary_updated_by_field_when_created(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual(glossary_obj.updated_by, self.user)

    def test_object_created_on_field_when_created(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual("2022-11-11 00:00:00+00:00", str(glossary_obj.created_on))
        self.assertNotEqual("", str(glossary_obj.created_on))

    def test_object_updated_on_field_when_created(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual("2022-11-11 00:00:00+00:00", str(glossary_obj.updated_on))
        self.assertNotEqual("", str(glossary_obj.updated_on))

    # Test whether object is updated properly

    def test_glossary_title_field_when_updated(self):
        glossary_obj = Glossary.objects.get(id=1)
        glossary_obj.title = "new title"
        glossary_obj.save()
        self.assertEqual(glossary_obj.title, "new title")
        self.assertNotEqual(glossary_obj.title, "test glossary")

    def test_glossary_notes_field_when_updated(self):
        glossary_obj = Glossary.objects.get(id=1)
        glossary_obj.notes = "A new note."
        glossary_obj.save()
        self.assertEqual(glossary_obj.notes, "A new note.")
        self.assertNotEqual(glossary_obj.notes, "Test note.")

    def test_glossary_updated_by_field_when_updated(self):
        glossary_obj = Glossary.objects.get(id=1)
        User = get_user_model()
        new_test_user = User.objects.create_user(
            username="new_test_user",
            email="new_test_user@email.com",
            password="testuser1234",
        )
        glossary_obj.updated_by = new_test_user
        glossary_obj.save()
        self.assertEqual(glossary_obj.updated_by, new_test_user)
        self.assertNotEqual(glossary_obj.updated_by, self.user)

    @freeze_time("2023-01-01")
    def test_object_updated_on_field_when_updated(self):
        glossary_obj = Glossary.objects.get(id=1)
        glossary_obj.title = "New Title"
        glossary_obj.save()
        self.assertEqual(str(glossary_obj.updated_on), "2023-01-01 00:00:00+00:00")
        self.assertNotEqual(str(glossary_obj.updated_on), "2022-11-11 00:00:00+00:00")

    # Check field properties

    def test_glossary_file_null_can_be_null(self):
        glossary_obj = Glossary.objects.get(id=1)
        null_bool = glossary_obj._meta.get_field("glossary_file").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_glossary_title_max_length(self):
        glossary_obj = Glossary.objects.get(id=1)
        max_length = glossary_obj._meta.get_field("glossary_file").max_length
        self.assertEqual(max_length, 100)

    def test_created_on_auto_now_add_is_true(self):
        glossary_obj = Glossary.objects.get(id=1)
        auto_now_add_bool = glossary_obj._meta.get_field("created_on").auto_now_add
        self.assertEqual(auto_now_add_bool, True)
        self.assertNotEqual(auto_now_add_bool, False)

    def test_updated_on_auto_now_add_is_true(self):
        glossary_obj = Glossary.objects.get(id=1)
        auto_now_bool = glossary_obj._meta.get_field("updated_on").auto_now
        self.assertEqual(auto_now_bool, True)
        self.assertNotEqual(auto_now_bool, False)

    def test_created_by_can_be_null(self):
        glossary_obj = Glossary.objects.get(id=1)
        null_bool = glossary_obj._meta.get_field("created_by").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_updated_by_can_be_null(self):
        glossary_obj = Glossary.objects.get(id=1)
        null_bool = glossary_obj._meta.get_field("updated_by").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_created_by_related_name(self):
        user_created_glossaries = self.user.created_glossaries.all()
        self.assertEqual(len(user_created_glossaries), 1)
        self.assertEqual(user_created_glossaries[0].title, "test glossary")

    def test_updated_by_related_name_when_glossary_created(self):
        user_updated_glossaries = self.user.updated_glossaries.all()
        self.assertEqual(len(user_updated_glossaries), 1)
        self.assertEqual(user_updated_glossaries[0].title, "test glossary")

    def test_updated_by_related_name_when_glossary_updated(self):
        glossary_obj = Glossary.objects.get(id=1)
        glossary_obj.title = "new test glossary"
        glossary_obj.save()
        user_updated_glossaries = self.user.updated_glossaries.all()
        self.assertEqual(len(user_updated_glossaries), 1)
        self.assertEqual(user_updated_glossaries[0].title, "new test glossary")
        self.assertNotEqual(user_updated_glossaries[0].title, "test glossary")

    def test_created_by_foreign_key_set_to_null_when_user_is_deleted(self):
        User = get_user_model()
        test_user_2 = User.objects.create_user(
            username="test_user_2",
            email="test_user_2@email.com",
            password="testuser1234",
        )
        new_glossary_2 = Glossary.objects.create(
            title="New Glossary 2",
            notes="Test note.",
            type="用語集",
            created_by=test_user_2,
            updated_by=test_user_2,
        )
        self.assertEqual(new_glossary_2.created_by, test_user_2)
        test_user_2.delete()
        # It is necessary to use Model.refresh_from_db() below because
        # new_glossary_2 still holds its initial values.
        # Using refresh_from_db() updates with up-to-date values.
        new_glossary_2.refresh_from_db()
        self.assertEqual(new_glossary_2.created_by, None)

    def test_updated_by_foreign_key_set_to_null_when_user_is_deleted(self):
        User = get_user_model()
        test_user_3 = User.objects.create_user(
            username="test_user_3",
            email="test_user_3@email.com",
            password="testuser1234",
        )
        new_glossary_3 = Glossary.objects.create(
            title="New Glossary 3",
            notes="Test note.",
            type="用語集",
            created_by=test_user_3,
            updated_by=test_user_3,
        )
        self.assertEqual(new_glossary_3.updated_by, test_user_3)
        test_user_3.delete()
        new_glossary_3.refresh_from_db()
        self.assertEqual(new_glossary_3.updated_by, None)

    # Check meta fields

    def test_verbose_name(self):
        glossary_obj = Glossary.objects.get(id=1)
        verbose_name = glossary_obj._meta.verbose_name
        self.assertEqual(verbose_name, "glossary")
        self.assertNotEqual(verbose_name, "")

    def test_verbose_name_plural(self):
        glossary_obj = Glossary.objects.get(id=1)
        verbose_name_plural = glossary_obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "glossaries")
        self.assertNotEqual(verbose_name_plural, "")
        self.assertNotEqual(verbose_name_plural, "glossary")

    # Check class methods

    def test_str_representation(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual(str(glossary_obj), "test glossary")
        self.assertNotEqual(str(glossary_obj), "")

    def test_absolute_url(self):
        glossary_obj = Glossary.objects.get(id=1)
        self.assertEqual(glossary_obj.get_absolute_url(), "/glossary/1/")
        self.assertNotEqual(glossary_obj.get_absolute_url(), "")
