from django.test import TestCase
from django.contrib.auth import get_user_model
from django.forms.widgets import Textarea, TextInput

from ...models import Entry, Glossary
from ...forms.entry_forms import EntryForm


"""
Form testing approach:
- Test fields
  - Labels, help text, and other properties you have set
- Test Meta fields
- Test form methods created yourself
- Test valid submission of complete form
- Test invalid submission of empty form
- Test invalid submissions with regard to each field
"""


class TestEntryForm(TestCase):

    @classmethod
    def setUpTestData(cls):

        # Test user
        User = get_user_model()
        cls.testuser = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testuser123",
        )

        # Glossary objects
        cls.glossary_obj_1 = Glossary.objects.create(
            title="Test Glossary 1",
            notes="Test note.",
            type="用語集",
            created_by=cls.testuser,
            updated_by=cls.testuser,
        )
        cls.glossary_obj_2 = Glossary.objects.create(
            title="Test Glossary 2",
            notes="Test note.",
            type="用語集",
            created_by=cls.testuser,
            updated_by=cls.testuser,
        )

        # Form with no input
        cls.empty_form = EntryForm()

        # Complete form with valid input (to add uploaded file content to existing glossary)
        cls.valid_form_with_existing_glossary = EntryForm(
            {
                "source": "テスト",
                "target": "test",
                "glossary": cls.glossary_obj_1,
                "new_glossary": "",
                "notes": "Some test notes.",
            }
        )

        # Complete form with valid input (to add uploaded file content to new glossary)
        cls.valid_form_with_new_glossary = EntryForm(
            {
                "source": "テスト",
                "target": "test",
                "glossary": None,
                "new_glossary": "Test Glossary",
                "notes": "Some test notes.",
            }
        )

    # Test fields

    def test_entry_source_field_label(self):
        self.assertEqual(
            self.empty_form.fields['source'].label,
            '① 原文'
        )

    def test_entry_source_field_label_required(self):
        self.assertTrue(self.empty_form.fields["source"].required)

    def test_entry_source_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['source'].error_messages['required'],
            'このフィールドは入力必須です。',
        )

    def test_entry_source_field_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields['source'].error_messages['max_length'],
            '255文字以下になるように変更してください。',
        )

    def test_target_source_field_label(self):
        self.assertEqual(
            self.empty_form.fields['target'].label,
            '② 訳文'
        )

    def test_target_source_field_label_required(self):
        self.assertTrue(self.empty_form.fields["target"].required)

    def test_target_source_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['target'].error_messages['required'],
            'このフィールドは入力必須です。',
        )

    def test_target_source_field_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields['target'].error_messages['max_length'],
            '255文字以下になるように変更してください。',
        )

    def test_glossary_field_label(self):
        self.assertEqual(
            self.empty_form.fields['glossary'].label,
            '③ 既存の用語集に関連付けますか？'
        )

    def test_glossary_field_queryset(self):
        expected = list(Glossary.objects.all().order_by('title'))
        existing_glossary_queryset = list(self.empty_form.fields['glossary'].queryset)
        self.assertEqual(existing_glossary_queryset, expected)

    def test_glossary_field_required(self):
        self.assertEqual(self.empty_form.fields['glossary'].required, False)

    def test_new_glossary_field_label(self):
        self.assertEqual(
            self.empty_form.fields['new_glossary'].label,
            '④ または、この用語のために新しい用語集を作成しますか？',
        )

    def test_new_glossary_field_widget(self):
        self.assertTrue(self.empty_form.fields['new_glossary'].widget, TextInput)
        self.assertEqual(
            self.empty_form.fields['new_glossary'].widget.attrs['placeholder'],
            '新しい用語集のタイトルを入力してください。',
        )

    def test_new_glossary_field_required(self):
        self.assertEqual(self.empty_form.fields['new_glossary'].required, False)

    def test_notes_field_label(self):
        self.assertEqual(self.empty_form.fields['notes'].label, '⑤ 備考（任意）')

    def test_notes_field_widget(self):
        self.assertTrue(self.empty_form.fields['notes'].widget, Textarea)
        self.assertEqual(self.empty_form.fields['notes'].widget.attrs['rows'], 6)

    def test_notes_field_required(self):
        self.assertEqual(self.empty_form.fields['notes'].required, False)

    # Test Meta fields

    def test_meta_model(self):
        self.assertEqual(self.empty_form._meta.model, Entry)

    def test_meta_fields(self):
        self.assertEqual(
            self.empty_form._meta.fields,
            ('source', 'target', 'glossary', 'new_glossary', 'notes'),
        )

    # Test valid forms

    def test_form_with_valid_input_add_to_existing_glossary(self):
        self.assertTrue(self.valid_form_with_existing_glossary.is_bound)
        self.assertTrue(self.valid_form_with_existing_glossary.is_valid())
        self.assertEqual(self.valid_form_with_existing_glossary.errors, {})
        self.assertEqual(self.valid_form_with_existing_glossary.errors.as_text(), "")
        self.assertEqual(self.valid_form_with_existing_glossary.cleaned_data["source"], "テスト")
        self.assertEqual(self.valid_form_with_existing_glossary.cleaned_data["target"], "test")
        self.assertEqual(
            self.valid_form_with_existing_glossary.cleaned_data["glossary"],
            self.glossary_obj_1
        )
        self.assertEqual(self.valid_form_with_existing_glossary.cleaned_data["new_glossary"], "")
        self.assertEqual(
            self.valid_form_with_existing_glossary.cleaned_data["notes"],
            "Some test notes.",
        )

    def test_form_with_valid_input_add_to_new_glossary(self):
        self.assertTrue(self.valid_form_with_new_glossary.is_bound)
        self.assertTrue(self.valid_form_with_new_glossary.is_valid())
        self.assertEqual(self.valid_form_with_new_glossary.errors, {})
        self.assertEqual(self.valid_form_with_new_glossary.errors.as_text(), "")
        self.assertEqual(self.valid_form_with_new_glossary.cleaned_data["source"], "テスト")
        self.assertEqual(self.valid_form_with_new_glossary.cleaned_data["target"], "test")
        self.assertEqual(self.valid_form_with_new_glossary.cleaned_data["glossary"], None)
        self.assertEqual(
            self.valid_form_with_new_glossary.cleaned_data["new_glossary"],
            "Test Glossary",
        )
        self.assertEqual(
            self.valid_form_with_new_glossary.cleaned_data["notes"],
            "Some test notes.",
        )

    # Test empty form

    def test_form_with_no_input(self):
        self.assertFalse(self.empty_form.is_bound)
        self.assertFalse(self.empty_form.is_valid())
        with self.assertRaises(AttributeError):
            self.empty_form.cleaned_data

    # Test invalid fields
