from django.test import TestCase
from django.forms.widgets import Textarea

from ...forms.glossary_forms import GlossaryForm
from ...models import Glossary

# from freezegun import freeze_time

# Test fields
# - Labels, help text, and other properties you have set
# Test Meta fields
# Test form methods created yourself


class TestGlossaryForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form = GlossaryForm()

    # Test fields

    def test_title_field_label(self):
        self.assertEqual(self.form.fields['title'].label, '用語集のタイトル')

    def test_title_field_required_error_message(self):
        self.assertEqual(
            self.form.fields['title'].error_messages['required'],
            'このフィールドは入力必須です。'
        )

    def test_notes_field_label(self):
        self.assertTrue(self.form.fields['notes'].label, '備考（任意）')

    def test_notes_field_required(self):
        self.assertFalse(self.form.fields['notes'].required)

    def test_notes_field_widget(self):
        self.assertTrue(self.form.fields['notes'].widget, Textarea)
        self.assertEqual(self.form.fields['notes'].widget.attrs['rows'], 6)

    # Test Meta fields

    def test_meta_model(self):
        self.assertEqual(self.form._meta.model, Glossary)

    def test_meta_fields(self):
        self.assertEqual(self.form._meta.fields, ('title', 'notes'))
