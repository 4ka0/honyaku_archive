from django.test import TestCase
from django.contrib.auth import get_user_model

from ...models import Resource

from freezegun import freeze_time


class ResourceModelTests(TestCase):

    @classmethod
    @freeze_time("2022-11-11")
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testuser123",
        )
        Resource.objects.create(
            resource_type="TRANSLATION",
            title="Test Resource",
            field="Chemical",
            client="ABC Co., Ltd.",
            translator="Graham Greene",
            notes="Test note.",
            created_by=cls.user,
            updated_by=cls.user,
        )

    # Check field labels are correct when object created

    def test_upload_file_file_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("upload_file").verbose_name
        self.assertEqual(field_label, "upload file")
        self.assertNotEqual(field_label, "upload_file")
        self.assertNotEqual(field_label, "")

    def test_resource_type_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("resource_type").verbose_name
        self.assertEqual(field_label, "resource type")
        self.assertNotEqual(field_label, "resource_type")
        self.assertNotEqual(field_label, "")

    def test_title_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")
        self.assertNotEqual(field_label, "")

    def test_field_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("field").verbose_name
        self.assertEqual(field_label, "field")
        self.assertNotEqual(field_label, "")

    def test_client_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("client").verbose_name
        self.assertEqual(field_label, "client")
        self.assertNotEqual(field_label, "")

    def test_translator_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("translator").verbose_name
        self.assertEqual(field_label, "translator")
        self.assertNotEqual(field_label, "")

    def test_notes_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("notes").verbose_name
        self.assertEqual(field_label, "notes")
        self.assertNotEqual(field_label, "")

    def test_created_by_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("created_by").verbose_name
        self.assertEqual(field_label, "created by")
        self.assertNotEqual(field_label, "created_by")
        self.assertNotEqual(field_label, "")

    def test_updated_by_label(self):
        resource = Resource.objects.get(id=1)
        field_label = resource._meta.get_field("updated_by").verbose_name
        self.assertEqual(field_label, "updated by")
        self.assertNotEqual(field_label, "updated_by")
        self.assertNotEqual(field_label, "")

    # Check field values are correct when object created

    def test_resource_type_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.resource_type, "TRANSLATION")
        self.assertNotEqual(resource.resource_type, "GLOSSARY")
        self.assertNotEqual(resource.resource_type, "")

    def test_title_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.title, "Test Resource")
        self.assertNotEqual(resource.title, "")

    def test_field_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.field, "Chemical")
        self.assertNotEqual(resource.field, "")

    def test_client_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.client, "ABC Co., Ltd.")
        self.assertNotEqual(resource.client, "")

    def test_translator_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.translator, "Graham Greene")
        self.assertNotEqual(resource.translator, "")

    def test_notes_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.notes, "Test note.")
        self.assertNotEqual(resource.notes, "")

    def test_object_created_on_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual("2022-11-11 00:00:00+00:00", str(resource.created_on))
        self.assertNotEqual("", str(resource.created_on))

    def test_glossary_created_by_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.created_by, self.user)

    def test_object_updated_on_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual("2022-11-11 00:00:00+00:00", str(resource.updated_on))
        self.assertNotEqual("", str(resource.updated_on))

    def test_glossary_updated_by_field_when_created(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.updated_by, self.user)

    # Check field values are correct when updated

    def test_resource_type_field_when_updated(self):
        resource = Resource.objects.get(id=1)
        resource.resource_type = "GLOSSARY"
        resource.save()
        self.assertEqual(resource.resource_type, "GLOSSARY")
        self.assertNotEqual(resource.resource_type, "TRANSLATION")
        self.assertNotEqual(resource.resource_type, "")

    def test_title_field_when_updated(self):
        resource = Resource.objects.get(id=1)
        resource.title = "New Title"
        resource.save()
        self.assertEqual(resource.title, "New Title")
        self.assertNotEqual(resource.title, "Test Resource")
        self.assertNotEqual(resource.title, "")

    def test_field_field_when_updated(self):
        resource = Resource.objects.get(id=1)
        resource.field = "Mechanical"
        resource.save()
        self.assertEqual(resource.field, "Mechanical")
        self.assertNotEqual(resource.field, "Chemical")
        self.assertNotEqual(resource.field, "")

    def test_client_field_when_updated(self):
        resource = Resource.objects.get(id=1)
        resource.client = "DEF Co., Ltd."
        resource.save()
        self.assertEqual(resource.client, "DEF Co., Ltd.")
        self.assertNotEqual(resource.client, "ABC Co., Ltd.")
        self.assertNotEqual(resource.client, "")

    def test_translator_field_when_updated(self):
        resource = Resource.objects.get(id=1)
        resource.translator = "David Mitchell"
        resource.save()
        self.assertEqual(resource.translator, "David Mitchell")
        self.assertNotEqual(resource.translator, "Graham Greene")
        self.assertNotEqual(resource.translator, "")

    def test_notes_field_when_updated(self):
        resource = Resource.objects.get(id=1)
        resource.notes = "Some new notes."
        resource.save()
        self.assertEqual(resource.notes, "Some new notes.")
        self.assertNotEqual(resource.notes, "Test note.")
        self.assertNotEqual(resource.notes, "")

    def test_updated_by_field_when_updated(self):
        resource = Resource.objects.get(id=1)
        User = get_user_model()
        new_test_user = User.objects.create_user(
            username="new_test_user",
            email="new_test_user@email.com",
            password="testuser1234",
        )
        resource.updated_by = new_test_user
        resource.save()
        self.assertEqual(resource.updated_by, new_test_user)
        self.assertNotEqual(resource.updated_by, self.user)

    @freeze_time("2023-01-01")
    def test_object_updated_on_field_when_updated(self):
        glossary_obj = Resource.objects.get(id=1)
        glossary_obj.title = "New Title"
        glossary_obj.save()
        self.assertEqual(str(glossary_obj.updated_on), "2023-01-01 00:00:00+00:00")
        self.assertNotEqual(str(glossary_obj.updated_on), "2022-11-11 00:00:00+00:00")

    # Check field properties

    def test_upload_file_null_can_be_null(self):
        resource = Resource.objects.get(id=1)
        null_bool = resource._meta.get_field("upload_file").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_resource_type_max_length(self):
        resource = Resource.objects.get(id=1)
        max_length = resource._meta.get_field("resource_type").max_length
        self.assertEqual(max_length, 20)
        self.assertNotEqual(max_length, 100)

    def test_title_max_length(self):
        resource = Resource.objects.get(id=1)
        max_length = resource._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_field_max_length(self):
        resource = Resource.objects.get(id=1)
        max_length = resource._meta.get_field("field").max_length
        self.assertEqual(max_length, 100)

    def test_field_blank(self):
        resource = Resource.objects.get(id=1)
        blank_bool = resource._meta.get_field("field").blank
        self.assertEqual(blank_bool, True)
        self.assertNotEqual(blank_bool, False)

    def test_client_max_length(self):
        resource = Resource.objects.get(id=1)
        max_length = resource._meta.get_field("client").max_length
        self.assertEqual(max_length, 100)

    def test_client_blank(self):
        resource = Resource.objects.get(id=1)
        blank_bool = resource._meta.get_field("client").blank
        self.assertEqual(blank_bool, True)
        self.assertNotEqual(blank_bool, False)

    def test_translator_max_length(self):
        resource = Resource.objects.get(id=1)
        max_length = resource._meta.get_field("translator").max_length
        self.assertEqual(max_length, 100)

    def test_translator_blank(self):
        resource = Resource.objects.get(id=1)
        blank_bool = resource._meta.get_field("translator").blank
        self.assertEqual(blank_bool, True)
        self.assertNotEqual(blank_bool, False)

    def test_notes_blank(self):
        resource = Resource.objects.get(id=1)
        blank_bool = resource._meta.get_field("notes").blank
        self.assertEqual(blank_bool, True)
        self.assertNotEqual(blank_bool, False)

    def test_created_on_auto_now_add_is_true(self):
        resource = Resource.objects.get(id=1)
        auto_now_add_bool = resource._meta.get_field("created_on").auto_now_add
        self.assertEqual(auto_now_add_bool, True)
        self.assertNotEqual(auto_now_add_bool, False)

    def test_updated_on_auto_now_is_true(self):
        resource = Resource.objects.get(id=1)
        auto_now_bool = resource._meta.get_field("updated_on").auto_now
        self.assertEqual(auto_now_bool, True)
        self.assertNotEqual(auto_now_bool, False)

    def test_created_by_can_be_null(self):
        resource = Resource.objects.get(id=1)
        null_bool = resource._meta.get_field("created_by").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_updated_by_can_be_null(self):
        resource = Resource.objects.get(id=1)
        null_bool = resource._meta.get_field("updated_by").null
        self.assertEqual(null_bool, True)
        self.assertNotEqual(null_bool, False)

    def test_created_by_related_name(self):
        user_created_resources = self.user.created_resources.all()
        self.assertEqual(len(user_created_resources), 1)
        self.assertEqual(user_created_resources[0].title, "Test Resource")

    def test_updated_by_related_name_when_glossary_created(self):
        user_updated_resources = self.user.updated_resources.all()
        self.assertEqual(len(user_updated_resources), 1)
        self.assertEqual(user_updated_resources[0].title, "Test Resource")

    def test_updated_by_related_name_when_glossary_updated(self):
        resource = Resource.objects.get(id=1)
        resource.title = "New Test Resource"
        resource.save()
        user_updated_resources = self.user.updated_resources.all()
        self.assertEqual(len(user_updated_resources), 1)
        self.assertEqual(user_updated_resources[0].title, "New Test Resource")
        self.assertNotEqual(user_updated_resources[0].title, "Test Resource")

    def test_created_by_foreign_key_set_to_null_when_user_is_deleted(self):
        User = get_user_model()
        test_user_2 = User.objects.create_user(
            username="test_user_2",
            email="test_user_2@email.com",
            password="testuser1234",
        )
        new_resource_2 = Resource.objects.create(
            resource_type="TRANSLATION",
            title="Test Resource 2",
            field="Chemical 2",
            client="ABC Co., Ltd. 2",
            translator="Graham Greene 2",
            notes="Test note 2.",
            created_by=test_user_2,
            updated_by=test_user_2,
        )
        self.assertEqual(new_resource_2.created_by, test_user_2)
        test_user_2.delete()
        # It is necessary to use Model.refresh_from_db() below because
        # new_glossary_2 still holds its initial values.
        # Using refresh_from_db() updates with up-to-date values.
        new_resource_2.refresh_from_db()
        self.assertEqual(new_resource_2.created_by, None)

    def test_updated_by_foreign_key_set_to_null_when_user_is_deleted(self):
        User = get_user_model()
        test_user_3 = User.objects.create_user(
            username="test_user_3",
            email="test_user_3@email.com",
            password="testuser1234",
        )
        new_resource_3 = Resource.objects.create(
            resource_type="TRANSLATION",
            title="Test Resource 3",
            field="Chemical 3",
            client="ABC Co., Ltd. 3",
            translator="Graham Greene 3",
            notes="Test note 3.",
            created_by=test_user_3,
            updated_by=test_user_3,
        )
        self.assertEqual(new_resource_3.updated_by, test_user_3)
        test_user_3.delete()
        new_resource_3.refresh_from_db()
        self.assertEqual(new_resource_3.updated_by, None)

    # Check meta fields

    def test_verbose_name(self):
        resource = Resource.objects.get(id=1)
        verbose_name = resource._meta.verbose_name
        self.assertEqual(verbose_name, "resource")
        self.assertNotEqual(verbose_name, "")

    def test_verbose_name_plural(self):
        resource = Resource.objects.get(id=1)
        verbose_name_plural = resource._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "resources")
        self.assertNotEqual(verbose_name_plural, "")
        self.assertNotEqual(verbose_name_plural, "resource")

    # Check class methods

    def test_str_representation(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(str(resource), "Test Resource")
        self.assertNotEqual(str(resource), "")

    def test_absolute_url(self):
        resource = Resource.objects.get(id=1)
        self.assertEqual(resource.get_absolute_url(), "/glossary/1/")
        self.assertNotEqual(resource.get_absolute_url(), "")
