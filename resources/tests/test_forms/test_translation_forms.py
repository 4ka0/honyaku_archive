from django.test import TestCase
from django.forms.widgets import Textarea, TextInput
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from ...models import Translation
from ...forms.translation_forms import TranslationUpdateForm, TranslationUploadForm


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


class TestTranslationUpdateForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.empty_form = TranslationUpdateForm()
        cls.valid_form = TranslationUpdateForm(
            {
                "job_number": "ABC-0123456",
                "field": "化学",
                "client": "ABC社",
                "translator": "Test Translator",
                "notes": "This is a translation for testing.",
            }
        )
        cls.invalid_form_1 = TranslationUpdateForm(
            {
                "job_number": "",
                "field": "化学",
                "client": "ABC社",
                "translator": "Test Translator",
                "notes": "This is a translation for testing.",
            }
        )
        long_text = ("Text exceeding 100 chars Text exceeding 100 chars"
                     "Text exceeding 100 chars Text exceeding 100 chars"
                     "Text exceeding 100 chars Text exceeding 100 chars")
        cls.invalid_form_2 = TranslationUpdateForm(
            {
                "job_number": long_text,
                "field": long_text,
                "client": long_text,
                "translator": long_text,
                "notes": "This is a translation for testing.",
            }
        )

    # Test fields

    def test_job_number_label(self):
        self.assertEqual(self.empty_form.fields['job_number'].label, '① 案件番号')

    def test_job_number_required(self):
        self.assertTrue(self.empty_form.fields["job_number"].required)

    def test_job_number_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['job_number'].error_messages['required'],
            'このフィールドは入力必須です。'
        )

    def test_job_number_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields['job_number'].error_messages['max_length'],
            '100文字以下になるように変更してください。'
        )

    def test_field_label(self):
        self.assertEqual(self.empty_form.fields['field'].label, '② 分野（任意）')

    def test_field_required(self):
        self.assertFalse(self.empty_form.fields["field"].required)

    def test_field_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields['field'].error_messages['max_length'],
            '100文字以下になるように変更してください。'
        )

    def test_client_label(self):
        self.assertEqual(self.empty_form.fields['client'].label, '③ クライアント（任意）')

    def test_client_required(self):
        self.assertFalse(self.empty_form.fields["client"].required)

    def test_client_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields['client'].error_messages['max_length'],
            '100文字以下になるように変更してください。'
        )

    def test_translator_label(self):
        self.assertEqual(self.empty_form.fields['translator'].label, '④ 翻訳者（任意）')

    def test_translator_required(self):
        self.assertFalse(self.empty_form.fields["translator"].required)

    def test_translator_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields['translator'].error_messages['max_length'],
            '100文字以下になるように変更してください。'
        )

    def test_notes_label(self):
        self.assertEqual(self.empty_form.fields['notes'].label, '⑤ 備考（任意）')

    def test_notes_required(self):
        self.assertFalse(self.empty_form.fields["notes"].required)

    def test_notes_widget(self):
        self.assertIsInstance(self.empty_form.fields['notes'].widget, Textarea)
        self.assertEqual(self.empty_form.fields['notes'].widget.attrs['rows'], 6)

    # Test Meta fields

    def test_meta_model(self):
        self.assertEqual(self.empty_form._meta.model, Translation)

    def test_meta_fields(self):
        self.assertEqual(
            self.empty_form._meta.fields,
            ("job_number", "translator", "field", "client", "notes"),
        )

    # Test form with input

    def test_form_with_valid_input(self):
        self.assertTrue(self.valid_form.is_bound)
        self.assertTrue(self.valid_form.is_valid())
        self.assertEqual(self.valid_form.errors, {})
        self.assertEqual(self.valid_form.errors.as_text(), "")
        self.assertEqual(self.valid_form.cleaned_data["job_number"], "ABC-0123456")
        self.assertEqual(self.valid_form.cleaned_data["field"], "化学")
        self.assertEqual(self.valid_form.cleaned_data["client"], "ABC社")
        self.assertEqual(self.valid_form.cleaned_data["translator"], "Test Translator")
        self.assertEqual(self.valid_form.cleaned_data["notes"], "This is a translation for testing.")

    def test_form_with_no_input(self):
        self.assertFalse(self.empty_form.is_bound)
        self.assertFalse(self.empty_form.is_valid())
        with self.assertRaises(AttributeError):
            self.empty_form.cleaned_data

    def test_form_with_invalid_input_blank_job_number(self):
        self.assertFalse(self.invalid_form_1.is_valid())
        self.assertNotEqual(self.invalid_form_1.errors, {})
        self.assertEqual(self.invalid_form_1.errors["job_number"], ["このフィールドは入力必須です。"])

    def test_form_with_invalid_input_job_number_too_long(self):
        self.assertFalse(self.invalid_form_2.is_valid())
        self.assertNotEqual(self.invalid_form_2.errors, {})
        self.assertEqual(
            self.invalid_form_2.errors["job_number"],
            ["100文字以下になるように変更してください。"]
        )

    def test_form_with_invalid_input_field_too_long(self):
        self.assertFalse(self.invalid_form_2.is_valid())
        self.assertNotEqual(self.invalid_form_2.errors, {})
        self.assertEqual(
            self.invalid_form_2.errors["field"],
            ["100文字以下になるように変更してください。"]
        )

    def test_form_with_invalid_input_client_too_long(self):
        self.assertFalse(self.invalid_form_2.is_valid())
        self.assertNotEqual(self.invalid_form_2.errors, {})
        self.assertEqual(
            self.invalid_form_2.errors["client"],
            ["100文字以下になるように変更してください。"]
        )

    def test_form_with_invalid_input_translator_too_long(self):
        self.assertFalse(self.invalid_form_2.is_valid())
        self.assertNotEqual(self.invalid_form_2.errors, {})
        self.assertEqual(
            self.invalid_form_2.errors["translator"],
            ["100文字以下になるように変更してください。"]
        )


class TestTranslationUploadForm(TestCase):
    pass
