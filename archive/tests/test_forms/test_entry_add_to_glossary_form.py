from django.test import TestCase
from django.forms.widgets import Textarea

from ...models import Entry
from ...forms.item_forms import EntryAddToGlossaryForm


class TestEntryAddToGlossaryForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Form with no input
        cls.empty_form = EntryAddToGlossaryForm()

        # Valid forms

        cls.valid_form_with_notes = EntryAddToGlossaryForm(
            {
                "source": "テスト",
                "target": "test",
                "notes": "Some test notes.",
            }
        )

        cls.valid_form_without_notes = EntryAddToGlossaryForm(
            {
                "source": "テスト",
                "target": "test",
                "notes": "",
            }
        )

        # Invalid forms

        cls.invalid_form_no_source = EntryAddToGlossaryForm(
            {
                "source": "",
                "target": "test",
                "notes": "Some test notes.",
            }
        )

        cls.invalid_form_no_target = EntryAddToGlossaryForm(
            {
                "source": "テスト",
                "target": "",
                "notes": "Some test notes.",
            }
        )

        cls.invalid_form_source_target_too_long = EntryAddToGlossaryForm(
            {
                "source": (
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                ),
                "target": (
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                ),
                "notes": "Some test notes.",
            }
        )

    # Test fields

    def test_entry_source_field_label(self):
        self.assertEqual(self.empty_form.fields["source"].label, "① 原文")

    def test_entry_source_field_label_required(self):
        self.assertTrue(self.empty_form.fields["source"].required)

    def test_entry_source_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields["source"].error_messages["required"],
            "このフィールドは入力必須です。",
        )

    def test_entry_source_field_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields["source"].error_messages["max_length"],
            "255文字以下になるように変更してください。",
        )

    def test_target_source_field_label(self):
        self.assertEqual(self.empty_form.fields["target"].label, "② 訳文")

    def test_target_source_field_label_required(self):
        self.assertTrue(self.empty_form.fields["target"].required)

    def test_target_source_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields["target"].error_messages["required"],
            "このフィールドは入力必須です。",
        )

    def test_target_source_field_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields["target"].error_messages["max_length"],
            "255文字以下になるように変更してください。",
        )

    def test_notes_field_label(self):
        self.assertEqual(self.empty_form.fields["notes"].label, "③ 備考（任意）")

    def test_notes_field_widget(self):
        self.assertIsInstance(self.empty_form.fields["notes"].widget, Textarea)
        self.assertEqual(self.empty_form.fields["notes"].widget.attrs["rows"], 6)

    def test_notes_field_required(self):
        self.assertEqual(self.empty_form.fields["notes"].required, False)

    # Test Meta fields

    def test_meta_model(self):
        self.assertEqual(self.empty_form._meta.model, Entry)

    def test_meta_fields(self):
        self.assertEqual(
            self.empty_form._meta.fields,
            ("source", "target", "notes"),
        )

    # Test valid forms

    def test_form_with_notes_valid_input(self):
        self.assertTrue(self.valid_form_with_notes.is_bound)
        self.assertTrue(self.valid_form_with_notes.is_valid())
        self.assertEqual(self.valid_form_with_notes.errors, {})
        self.assertEqual(self.valid_form_with_notes.errors.as_text(), "")
        self.assertEqual(self.valid_form_with_notes.cleaned_data["source"], "テスト")
        self.assertEqual(self.valid_form_with_notes.cleaned_data["target"], "test")
        self.assertEqual(
            self.valid_form_with_notes.cleaned_data["notes"], "Some test notes."
        )

    def test_form_without_notes_valid_input(self):
        self.assertTrue(self.valid_form_without_notes.is_bound)
        self.assertTrue(self.valid_form_without_notes.is_valid())
        self.assertEqual(self.valid_form_without_notes.errors, {})
        self.assertEqual(self.valid_form_without_notes.errors.as_text(), "")
        self.assertEqual(self.valid_form_without_notes.cleaned_data["source"], "テスト")
        self.assertEqual(self.valid_form_without_notes.cleaned_data["target"], "test")
        self.assertEqual(self.valid_form_without_notes.cleaned_data["notes"], "")

    # Test empty form

    def test_form_with_no_input(self):
        self.assertFalse(self.empty_form.is_bound)
        self.assertFalse(self.empty_form.is_valid())
        with self.assertRaises(AttributeError):
            self.empty_form.cleaned_data

    # Test invalid fields

    def test_form_with_invalid_input_no_source(self):
        self.assertFalse(self.invalid_form_no_source.is_valid())
        self.assertNotEqual(self.invalid_form_no_source.errors, {})
        self.assertEqual(
            self.invalid_form_no_source.errors["source"], ["このフィールドは入力必須です。"]
        )

    def test_form_with_invalid_input_no_target(self):
        self.assertFalse(self.invalid_form_no_target.is_valid())
        self.assertNotEqual(self.invalid_form_no_target.errors, {})
        self.assertEqual(
            self.invalid_form_no_target.errors["target"], ["このフィールドは入力必須です。"]
        )

    def test_form_with_invalid_input_source_too_long(self):
        self.assertFalse(self.invalid_form_source_target_too_long.is_valid())
        self.assertNotEqual(self.invalid_form_source_target_too_long.errors, {})
        self.assertEqual(
            self.invalid_form_source_target_too_long.errors["source"],
            ["255文字以下になるように変更してください。"],
        )

    def test_form_with_invalid_input_target_too_long(self):
        self.assertFalse(self.invalid_form_source_target_too_long.is_valid())
        self.assertNotEqual(self.invalid_form_source_target_too_long.errors, {})
        self.assertEqual(
            self.invalid_form_source_target_too_long.errors["target"],
            ["255文字以下になるように変更してください。"],
        )
