from django.test import TestCase
from django.forms.widgets import Textarea

from ...models import Glossary
from ...forms.glossary_forms import GlossaryForm


class TestGlossaryForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.empty_form = GlossaryForm()
        cls.valid_form = GlossaryForm(
            {
                "title": "Test Glossary 1",
                "notes": "This is a glossary for testing.",
            }
        )
        cls.invalid_form_1 = GlossaryForm(
            {
                "title": "",
                "notes": "This is a glossary for testing.",
            }
        )
        cls.invalid_form_2 = GlossaryForm(
            {
                "title": ("Title exceeding 100 chars Title exceeding 100 chars"
                          "Title exceeding 100 chars Title exceeding 100 chars"),
                "notes": "This is a glossary for testing.",
            }
        )

    # Test fields

    def test_title_field_label(self):
        self.assertEqual(self.empty_form.fields['title'].label, '① 用語集のタイトル')

    def test_title_field_required(self):
        self.assertTrue(self.empty_form.fields["title"].required)

    def test_title_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['title'].error_messages['required'],
            'このフィールドは入力必須です。'
        )

    def test_title_field_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields['title'].error_messages['max_length'],
            '100文字以下になるように変更してください。'
        )

    def test_notes_field_label(self):
        self.assertEqual(self.empty_form.fields['notes'].label, '② 備考（任意）')

    def test_notes_field_required(self):
        self.assertFalse(self.empty_form.fields['notes'].required)

    def test_notes_field_widget(self):
        self.assertIsInstance(self.empty_form.fields['notes'].widget, Textarea)
        self.assertEqual(self.empty_form.fields['notes'].widget.attrs['rows'], 6)

    # Test Meta fields

    def test_meta_model(self):
        self.assertEqual(self.empty_form._meta.model, Glossary)

    def test_meta_fields(self):
        self.assertEqual(self.empty_form._meta.fields, ('title', 'notes'))

    # Test form with input

    def test_form_with_valid_input(self):
        self.assertTrue(self.valid_form.is_bound)
        self.assertTrue(self.valid_form.is_valid())
        self.assertEqual(self.valid_form.errors, {})
        self.assertEqual(self.valid_form.errors.as_text(), "")
        self.assertEqual(self.valid_form.cleaned_data["title"], "Test Glossary 1")
        self.assertEqual(self.valid_form.cleaned_data["notes"], "This is a glossary for testing.")

    def test_form_with_no_input(self):
        self.assertFalse(self.empty_form.is_bound)
        self.assertFalse(self.empty_form.is_valid())
        with self.assertRaises(AttributeError):
            self.empty_form.cleaned_data

    def test_form_with_invalid_input_blank_title(self):
        self.assertFalse(self.invalid_form_1.is_valid())
        self.assertNotEqual(self.invalid_form_1.errors, {})
        self.assertEqual(self.invalid_form_1.errors["title"], ["このフィールドは入力必須です。"])

    def test_form_with_invalid_input_title_too_long(self):
        self.assertFalse(self.invalid_form_2.is_valid())
        self.assertNotEqual(self.invalid_form_2.errors, {})
        self.assertEqual(
            self.invalid_form_2.errors["title"],
            ["100文字以下になるように変更してください。"]
        )
