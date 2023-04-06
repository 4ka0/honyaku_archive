from django.test import TestCase
from django.forms.widgets import Textarea

from ...models import Segment
from ...forms.segment_forms import SegmentForm


class TestEntryForm(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.empty_form = SegmentForm()

        cls.valid_form = SegmentForm(
            {
                "source": "テスト",
                "target": "test",
            }
        )

        cls.invalid_form_no_source_or_target = SegmentForm(
            {
                "source": "",
                "target": "",
            }
        )

    # Test fields

    # Source field

    def test_source_field_label(self):
        self.assertEqual(
            self.empty_form.fields['source'].label,
            '① 原文'
        )

    def test_source_field_label_required(self):
        self.assertTrue(self.empty_form.fields["source"].required)

    def test_source_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['source'].error_messages['required'],
            'このフィールドは入力必須です。',
        )

    def test_source_field_widget(self):
        self.assertIsInstance(self.empty_form.fields['source'].widget, Textarea)
        self.assertEqual(self.empty_form.fields['source'].widget.attrs['rows'], 6)

    # Target field

    def test_target_field_label(self):
        self.assertEqual(
            self.empty_form.fields['target'].label,
            '② 訳文'
        )

    def test_target_field_label_required(self):
        self.assertTrue(self.empty_form.fields["target"].required)

    def test_target_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['target'].error_messages['required'],
            'このフィールドは入力必須です。',
        )

    def test_target_field_widget(self):
        self.assertIsInstance(self.empty_form.fields['target'].widget, Textarea)
        self.assertEqual(self.empty_form.fields['target'].widget.attrs['rows'], 6)

    # Test Meta fields

    def test_meta_model(self):
        self.assertEqual(self.empty_form._meta.model, Segment)

    def test_meta_fields(self):
        self.assertEqual(
            self.empty_form._meta.fields,
            ('source', 'target'),
        )

    # Test valid form

    def test_valid_form(self):
        self.assertTrue(self.valid_form.is_bound)
        self.assertTrue(self.valid_form.is_valid())
        self.assertEqual(self.valid_form.errors, {})
        self.assertEqual(self.valid_form.errors.as_text(), "")
        self.assertEqual(self.valid_form.cleaned_data["source"], "テスト")
        self.assertEqual(self.valid_form.cleaned_data["target"], "test")

    # Test empty form

    def test_empty_form(self):
        self.assertFalse(self.empty_form.is_bound)
        self.assertFalse(self.empty_form.is_valid())
        with self.assertRaises(AttributeError):
            self.empty_form.cleaned_data

    # Test invalid fields

    def test_form_with_invalid_input_no_source(self):
        self.assertFalse(self.invalid_form_no_source_or_target.is_valid())
        self.assertNotEqual(self.invalid_form_no_source_or_target.errors, {})
        self.assertEqual(
            self.invalid_form_no_source_or_target.errors["source"],
            ["このフィールドは入力必須です。"],
        )

    def test_form_with_invalid_input_no_target(self):
        self.assertFalse(self.invalid_form_no_source_or_target.is_valid())
        self.assertNotEqual(self.invalid_form_no_source_or_target.errors, {})
        self.assertEqual(
            self.invalid_form_no_source_or_target.errors["target"],
            ["このフィールドは入力必須です。"],
        )
