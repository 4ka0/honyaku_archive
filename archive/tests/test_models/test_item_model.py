from django.test import TestCase
from django.contrib.auth import get_user_model

from ...models import Resource, Item

from freezegun import freeze_time


class ItemModelTests(TestCase):

    @classmethod
    @freeze_time("2022-11-11")
    def setUpTestData(cls):
        User = get_user_model()
        cls.testuser = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testuser123",
        )
        cls.resource = Resource.objects.create(
            resource_type="TRANSLATION",
            title="Test Resource",
            field="Chemical",
            client="ABC Co., Ltd.",
            translator="Graham Greene",
            notes="Test note.",
            created_by=cls.testuser,
            updated_by=cls.testuser,
        )
        cls.item = Item.objects.create(
            resource=cls.resource,
            source="テスト",
            target="test",
            notes="Just a test.",
            created_by=cls.testuser,
            updated_by=cls.testuser,
        )

    # Check field labels are correct when object created

    def test_resource_label(self):
        field_label = self.item._meta.get_field("resource").verbose_name
        self.assertEqual(field_label, "resource")
        self.assertNotEqual(field_label, "")

    def test_source_label(self):
        field_label = self.item._meta.get_field("source").verbose_name
        self.assertEqual(field_label, "source")
        self.assertNotEqual(field_label, "")

    def test_target_label(self):
        field_label = self.item._meta.get_field("target").verbose_name
        self.assertEqual(field_label, "target")
        self.assertNotEqual(field_label, "")

    def test_created_on_label(self):
        field_label = self.item._meta.get_field("created_on").verbose_name
        self.assertEqual(field_label, "created on")
        self.assertNotEqual(field_label, "created_on")
        self.assertNotEqual(field_label, "")

    def test_created_by_label(self):
        field_label = self.item._meta.get_field("created_by").verbose_name
        self.assertEqual(field_label, "created by")
        self.assertNotEqual(field_label, "created_by")
        self.assertNotEqual(field_label, "")

    def test_updated_on_label(self):
        field_label = self.item._meta.get_field("updated_on").verbose_name
        self.assertEqual(field_label, "updated on")
        self.assertNotEqual(field_label, "updated_on")
        self.assertNotEqual(field_label, "")

    def test_updated_by_label(self):
        field_label = self.item._meta.get_field("updated_by").verbose_name
        self.assertEqual(field_label, "updated by")
        self.assertNotEqual(field_label, "updated_by")
        self.assertNotEqual(field_label, "")

    # Up to here
    # Check field values are correct when object created

    def test_resource_field_when_created(self):
        self.assertEqual(self.item.Resource, self.resource)
        self.assertNotEqual(self.item.Resource, None)

    def test_source_field_when_created(self):
        self.assertEqual(self.item.source, "テスト")
        self.assertNotEqual(self.item.source, "")

    def test_target_field_when_created(self):
        self.assertEqual(self.item.target, "test")
        self.assertNotEqual(self.item.target, "")

    def test_notes_field_when_created(self):
        self.assertEqual(self.item.notes, "Just a test.")
        self.assertNotEqual(self.item.notes, "")

    def test_created_by_field_when_created(self):
        self.assertEqual(self.item.created_by, self.testuser)

    def test_updated_by_field_when_created(self):
        self.assertEqual(self.item.updated_by, self.testuser)

    def test_created_on_field_when_created(self):
        self.assertEqual("2022-11-11 00:00:00+00:00", str(self.item.created_on))
        self.assertNotEqual("", str(self.item.created_on))

    def test_updated_on_field_when_created(self):
        self.assertEqual("2022-11-11 00:00:00+00:00", str(self.item.updated_on))
        self.assertNotEqual("", str(self.item.updated_on))

    # Check field values are correct when updated

    def test_Resource_field_when_updated(self):
        new_resource = Resource.objects.create(
            title="Test Resource 1",
            notes="Test note 2.",
            type="用語集",
            created_by=self.testuser,
            updated_by=self.testuser,
        )
        self.item.Resource = new_resource
        self.item.save()
        self.assertEqual(self.item.Resource, new_resource)
        self.assertEqual(self.item.Resource.title, "Test Resource 1")
        self.assertNotEqual(self.item.Resource, self.resource)

    def test_source_field_when_updated(self):
        self.item.source = "情報"
        self.item.save()
        self.assertEqual(self.item.source, "情報")
        self.assertNotEqual(self.item.source, "テスト")

    def test_target_field_when_updated(self):
        self.item.target = "information"
        self.item.save()
        self.assertEqual(self.item.target, "information")
        self.assertNotEqual(self.item.target, "test")

    def test_created_by_field_when_updated(self):
        User = get_user_model()
        new_testuser = User.objects.create_user(
            username="new_test_user",
            email="new_test_user@email.com",
            password="testuser1234",
        )
        self.item.created_by = new_testuser
        self.item.save()
        self.assertEqual(self.item.created_by, new_testuser)
        self.assertNotEqual(self.item.created_by, self.testuser)

    def test_updated_by_field_when_updated(self):
        User = get_user_model()
        new_testuser = User.objects.create_user(
            username="new_test_user",
            email="new_test_user@email.com",
            password="testuser1234",
        )
        self.item.updated_by = new_testuser
        self.item.save()
        self.assertEqual(self.item.updated_by, new_testuser)
        self.assertNotEqual(self.item.updated_by, self.testuser)

    @freeze_time("2023-01-01")
    def test_object_updated_on_field_when_updated(self):
        self.item.source = "情報"
        self.item.save()
        self.assertEqual(str(self.item.updated_on), "2023-01-01 00:00:00+00:00")
        self.assertNotEqual(str(self.item.updated_on), "2022-11-11 00:00:00+00:00")

    # Check field properties

    def test_Item_deleted_when_Resource_deleted(self):
        new_resource = Resource.objects.create(
            title="Test Resource 3",
            notes="Test note.",
            type="用語集",
            created_by=self.testuser,
            updated_by=self.testuser,
        )
        Item.objects.create(
            resource=new_resource,
            source="装置",
            target="device",
            notes="Just a test.",
            created_by=self.testuser,
            updated_by=self.testuser,
        )
        self.assertEqual(Resource.objects.filter(title="Test Resource 3").count(), 1)
        self.assertEqual(Item.objects.filter(resource=new_resource).count(), 1)
        new_resource.delete()
        self.assertEqual(Resource.objects.filter(title="Test Resource 3").count(), 0)
        self.assertEqual(Item.objects.filter(resource=new_resource).count(), 0)

    def test_source_max_length(self):
        max_length = self.item._meta.get_field("source").max_length
        self.assertEqual(max_length, 255)

    def test_target_max_length(self):
        max_length = self.item._meta.get_field("target").max_length
        self.assertEqual(max_length, 255)

    def test_notes_blank_is_true(self):
        blank_bool = self.item._meta.get_field("notes").blank
        self.assertEqual(blank_bool, True)
        self.assertNotEqual(blank_bool, False)

    def test_created_on_auto_now_add_is_true(self):
        auto_now_add_bool = self.item._meta.get_field("created_on").auto_now_add
        self.assertEqual(auto_now_add_bool, True)
        self.assertNotEqual(auto_now_add_bool, False)

    def test_updated_on_auto_now_is_true(self):
        auto_now_bool = self.item._meta.get_field("updated_on").auto_now
        self.assertEqual(auto_now_bool, True)
        self.assertNotEqual(auto_now_bool, False)

    def test_created_by_can_be_null(self):
        null_bool = self.item._meta.get_field("created_by").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_updated_by_can_be_null(self):
        null_bool = self.item._meta.get_field("updated_by").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_created_by_related_name(self):
        user_created_entries = self.testuser.created_entries.all()
        self.assertEqual(len(user_created_entries), 1)
        self.assertEqual(user_created_entries[0].source, "テスト")
        self.assertEqual(user_created_entries[0].target, "test")

    def test_updated_by_related_name_when_Item_created(self):
        user_updated_entries = self.testuser.updated_entries.all()
        self.assertEqual(len(user_updated_entries), 1)
        self.assertEqual(user_updated_entries[0].source, "テスト")
        self.assertEqual(user_updated_entries[0].target, "test")

    def test_updated_by_related_name_when_Item_updated(self):
        self.item.source = "概念"
        self.item.save()
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
        new_resource_2 = Resource.objects.create(
            title="New Resource 2",
            notes="Test note.",
            type="用語集",
            created_by=testuser_2,
            updated_by=testuser_2,
        )
        new_Item_2 = Item.objects.create(
            resource=new_resource_2,
            source="コミュニケーション",
            target="communication",
            notes="Just a test.",
            created_by=testuser_2,
            updated_by=testuser_2,
        )
        self.assertEqual(new_Item_2.created_by, testuser_2)
        testuser_2.delete()
        new_Item_2.refresh_from_db()
        self.assertEqual(new_Item_2.created_by, None)

    def test_updated_by_foreign_key_set_to_null_when_user_is_deleted(self):
        User = get_user_model()
        testuser_3 = User.objects.create_user(
            username="testuser_2",
            email="test_user_2@email.com",
            password="testuser1234",
        )
        new_Resource_3 = Resource.objects.create(
            title="New Resource 2",
            notes="Test note.",
            type="用語集",
            created_by=testuser_3,
            updated_by=testuser_3,
        )
        new_Item_3 = Item.objects.create(
            resource=new_Resource_3,
            source="コミュニケーション",
            target="communication",
            notes="Just a test.",
            created_by=testuser_3,
            updated_by=testuser_3,
        )
        self.assertEqual(new_Item_3.updated_by, testuser_3)
        testuser_3.delete()
        new_Item_3.refresh_from_db()
        self.assertEqual(new_Item_3.updated_by, None)

    # Check meta fields

    def test_verbose_name(self):
        verbose_name = self.item._meta.verbose_name
        self.assertEqual(verbose_name, "Item")
        self.assertNotEqual(verbose_name, "")

    def test_verbose_name_plural(self):
        verbose_name_plural = self.item._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "entries")
        self.assertNotEqual(verbose_name_plural, "")
        self.assertNotEqual(verbose_name_plural, "Item")

    # Check class methods

    def test_str_representation(self):
        self.assertEqual(str(self.item), "テスト : test")
        self.assertNotEqual(str(self.item), "")
