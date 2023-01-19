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

    def test_glossary_field_when_created(self):
        self.assertEqual(self.entry_obj.glossary, self.glossary_obj)
        self.assertNotEqual(self.entry_obj.glossary, None)

    def test_source_field_when_created(self):
        self.assertEqual(self.entry_obj.source, "テスト")
        self.assertNotEqual(self.entry_obj.source, "")

    def test_target_field_when_created(self):
        self.assertEqual(self.entry_obj.target, "test")
        self.assertNotEqual(self.entry_obj.target, "")

    def test_notes_field_when_created(self):
        self.assertEqual(self.entry_obj.notes, "Just a test.")
        self.assertNotEqual(self.entry_obj.notes, "")

    def test_created_by_field_when_created(self):
        self.assertEqual(self.entry_obj.created_by, self.testuser)

    def test_updated_by_field_when_created(self):
        self.assertEqual(self.entry_obj.updated_by, self.testuser)

    def test_created_on_field_when_created(self):
        self.assertEqual("2022-11-11 00:00:00+00:00", str(self.entry_obj.created_on))
        self.assertNotEqual("", str(self.entry_obj.created_on))

    def test_updated_on_field_when_created(self):
        self.assertEqual("2022-11-11 00:00:00+00:00", str(self.entry_obj.updated_on))
        self.assertNotEqual("", str(self.entry_obj.updated_on))

    # Check field values are correct when updated

    def test_glossary_field_when_updated(self):
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

    def test_source_field_when_updated(self):
        self.entry_obj.source = "情報"
        self.entry_obj.save()
        self.assertEqual(self.entry_obj.source, "情報")
        self.assertNotEqual(self.entry_obj.source, "テスト")

    def test_target_field_when_updated(self):
        self.entry_obj.target = "information"
        self.entry_obj.save()
        self.assertEqual(self.entry_obj.target, "information")
        self.assertNotEqual(self.entry_obj.target, "test")

    def test_created_by_field_when_updated(self):
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

    def test_updated_by_field_when_updated(self):
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

    # Check field properties

    def test_entry_deleted_when_glossary_deleted(self):
        new_glossary_obj = Glossary.objects.create(
            title="Test Glossary 3",
            notes="Test note.",
            type="用語集",
            created_by=self.testuser,
            updated_by=self.testuser,
        )
        Entry.objects.create(
            glossary=new_glossary_obj,
            source="装置",
            target="device",
            notes="Just a test.",
            created_by=self.testuser,
            updated_by=self.testuser,
        )
        self.assertEqual(Glossary.objects.filter(title="Test Glossary 3").count(), 1)
        self.assertEqual(Entry.objects.filter(glossary=new_glossary_obj).count(), 1)
        new_glossary_obj.delete()
        self.assertEqual(Glossary.objects.filter(title="Test Glossary 3").count(), 0)
        self.assertEqual(Entry.objects.filter(glossary=new_glossary_obj).count(), 0)

    def test_source_max_length(self):
        max_length = self.entry_obj._meta.get_field("source").max_length
        self.assertEqual(max_length, 250)

    def test_target_max_length(self):
        max_length = self.entry_obj._meta.get_field("target").max_length
        self.assertEqual(max_length, 250)

    def test_notes_blank_is_true(self):
        blank_bool = self.entry_obj._meta.get_field("notes").blank
        self.assertEqual(blank_bool, True)
        self.assertNotEqual(blank_bool, False)

    def test_created_on_auto_now_add_is_true(self):
        auto_now_add_bool = self.entry_obj._meta.get_field("created_on").auto_now_add
        self.assertEqual(auto_now_add_bool, True)
        self.assertNotEqual(auto_now_add_bool, False)

    def test_updated_on_auto_now_is_true(self):
        auto_now_bool = self.entry_obj._meta.get_field("updated_on").auto_now
        self.assertEqual(auto_now_bool, True)
        self.assertNotEqual(auto_now_bool, False)

    def test_created_by_can_be_null(self):
        null_bool = self.entry_obj._meta.get_field("created_by").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_updated_by_can_be_null(self):
        null_bool = self.entry_obj._meta.get_field("updated_by").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_created_by_related_name(self):
        user_created_entries = self.testuser.created_entries.all()
        self.assertEqual(len(user_created_entries), 1)
        self.assertEqual(user_created_entries[0].source, "テスト")
        self.assertEqual(user_created_entries[0].target, "test")

    def test_updated_by_related_name_when_entry_created(self):
        user_updated_entries = self.testuser.updated_entries.all()
        self.assertEqual(len(user_updated_entries), 1)
        self.assertEqual(user_updated_entries[0].source, "テスト")
        self.assertEqual(user_updated_entries[0].target, "test")

    def test_updated_by_related_name_when_entry_updated(self):
        self.entry_obj.source = "概念"
        self.entry_obj.save()
        user_updated_entries = self.testuser.updated_entries.all()
        self.assertEqual(len(user_updated_entries), 1)
        self.assertEqual(user_updated_entries[0].source, "概念")
        self.assertNotEqual(user_updated_entries[0].source, "テスト")

    def test_created_by_foreign_key_set_to_null_when_user_is_deleted(self):
        User = get_user_model()
        testuser_2 = User.objects.create_user(
            username="testuser_2",
            email="test_user_2@email.com",
            password="testuser1234",
        )
        new_glossary_2 = Glossary.objects.create(
            title="New Glossary 2",
            notes="Test note.",
            type="用語集",
            created_by=testuser_2,
            updated_by=testuser_2,
        )
        new_entry_2 = Entry.objects.create(
            glossary=new_glossary_2,
            source="コミュニケーション",
            target="communication",
            notes="Just a test.",
            created_by=testuser_2,
            updated_by=testuser_2,
        )
        self.assertEqual(new_entry_2.created_by, testuser_2)
        testuser_2.delete()
        new_entry_2.refresh_from_db()
        self.assertEqual(new_entry_2.created_by, None)

    def test_updated_by_foreign_key_set_to_null_when_user_is_deleted(self):
        User = get_user_model()
        testuser_3 = User.objects.create_user(
            username="testuser_2",
            email="test_user_2@email.com",
            password="testuser1234",
        )
        new_glossary_3 = Glossary.objects.create(
            title="New Glossary 2",
            notes="Test note.",
            type="用語集",
            created_by=testuser_3,
            updated_by=testuser_3,
        )
        new_entry_3 = Entry.objects.create(
            glossary=new_glossary_3,
            source="コミュニケーション",
            target="communication",
            notes="Just a test.",
            created_by=testuser_3,
            updated_by=testuser_3,
        )
        self.assertEqual(new_entry_3.updated_by, testuser_3)
        testuser_3.delete()
        new_entry_3.refresh_from_db()
        self.assertEqual(new_entry_3.updated_by, None)

    # Check meta fields

    def test_verbose_name(self):
        verbose_name = self.entry_obj._meta.verbose_name
        self.assertEqual(verbose_name, "entry")
        self.assertNotEqual(verbose_name, "")

    def test_verbose_name_plural(self):
        verbose_name_plural = self.entry_obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "entries")
        self.assertNotEqual(verbose_name_plural, "")
        self.assertNotEqual(verbose_name_plural, "entry")

    # Check class methods

    def test_str_representation(self):
        self.assertEqual(str(self.entry_obj), "テスト : test")
        self.assertNotEqual(str(self.entry_obj), "")
