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
