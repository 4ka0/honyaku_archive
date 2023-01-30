from django.test import TestCase
from django.forms.widgets import Textarea, TextInput
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile


from ...models import Glossary
from ...forms.glossary_forms import GlossaryForm, GlossaryUploadForm

# from freezegun import freeze_time

# Test fields
# - Labels, help text, and other properties you have set
# Test Meta fields
# Test form methods created yourself
# Test empty submission
# Test complete submission
# Test validation edge cases


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
                "title": "Title exceeding 100 chars Title exceeding 100 chars Title exceeding 100 chars Title exceeding 100 chars",
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
        self.assertTrue(self.empty_form.fields['notes'].widget, Textarea)
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
        self.assertEqual(self.invalid_form_2.errors["title"], ["100文字以下になるように変更してください。"])


class TestGlossaryUploadForm(TestCase):

    @classmethod
    def setUpTestData(cls):

        # Test user
        User = get_user_model()
        cls.testuser = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testuser123",
        )

        # Glossary object
        cls.glossary_obj = Glossary.objects.create(
            title="test glossary",
            notes="Test note.",
            type="用語集",
            created_by=cls.testuser,
            updated_by=cls.testuser,
        )

        # Form with no input
        cls.empty_form = GlossaryUploadForm()

        # Form with input (to add uploaded file content to existing glossary)
        form_data = {
            "existing_glossary": cls.glossary_obj,
            "title": "",
            "notes": "Some test notes.",
        }
        file_data = {
            "glossary_file": SimpleUploadedFile(name='test_glossary_file.txt',
                                                content=b'file_content',
                                                content_type="text/plain"),
        }
        cls.valid_form_with_existing_glossary = GlossaryUploadForm(form_data, file_data)

    # Test fields

    def test_glossary_file_field_label(self):
        self.assertEqual(self.empty_form.fields['glossary_file'].label, '① ファイルを選択してください。')

    def test_glossary_file_field_required(self):
        self.assertTrue(self.empty_form.fields["glossary_file"].required)

    def test_glossary_file_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['glossary_file'].error_messages['required'],
            'このフィールドは入力必須です。'
        )

    def test_glossary_file_field_validators_len(self):
        self.assertEqual(len(self.empty_form.fields['glossary_file'].validators), 1)

    def test_glossary_file_field_validator_type(self):
        self.assertEqual(
            type(self.empty_form.fields['glossary_file'].validators[0]),
            FileExtensionValidator
        )

    def test_glossary_file_field_validator_allowed_extensions(self):
        self.assertEqual(
            self.empty_form.fields['glossary_file'].validators[0].allowed_extensions,
            ["txt"]
        )

    def test_glossary_file_field_validators_allowed_extensions_error_message(self):
        self.assertEqual(
            self.empty_form.fields['glossary_file'].validators[0].message,
            ['拡張子が".txt "のファイルを選択してください。']
        )

    def test_existing_glossary_field_label(self):
        self.assertEqual(self.empty_form.fields['existing_glossary'].label, '② 既存の用語集に追加しますか？')

    def test_existing_glossary_field_queryset(self):
        expected = list(Glossary.objects.all().order_by('title'))
        existing_glossary_queryset = list(self.empty_form.fields['existing_glossary'].queryset)
        self.assertEqual(existing_glossary_queryset, expected)

    def test_existing_glossary_field_required(self):
        self.assertEqual(self.empty_form.fields['existing_glossary'].required, False)

    def test_title_field_label(self):
        self.assertEqual(self.empty_form.fields['title'].label, '③ または、新しい用語集を作成しますか？')

    def test_title_field_widget(self):
        self.assertTrue(self.empty_form.fields['title'].widget, TextInput)
        self.assertEqual(
            self.empty_form.fields['title'].widget.attrs['placeholder'],
            '新しい用語集のタイトルを入力してください。'
        )

    def test_title_field_required(self):
        self.assertEqual(self.empty_form.fields['title'].required, False)

    def test_title_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['title'].error_messages['max_length'],
            '100文字以下になるように変更してください。'
        )

    def test_notes_field_label(self):
        self.assertEqual(self.empty_form.fields['notes'].label, '④ 備考（任意）')

    def test_notes_field_widget(self):
        self.assertTrue(self.empty_form.fields['notes'].widget, Textarea)
        self.assertEqual(self.empty_form.fields['notes'].widget.attrs['rows'], 6)

    def test_notes_field_required(self):
        self.assertEqual(self.empty_form.fields['notes'].required, False)

    def test_notes_field_help_text(self):
        self.assertEqual(
            self.empty_form.fields['notes'].help_text,
            "アップロードされる用語集は既存の用語集に追加する場合、<br>上記の備考は既存の用語集の備考に追加されます。"
        )

    # Test Meta fields

    def test_meta_model(self):
        self.assertEqual(self.empty_form._meta.model, Glossary)

    def test_meta_fields(self):
        self.assertEqual(self.empty_form._meta.fields, ("glossary_file", "existing_glossary", "title", "notes"))

    # Test complete form

    def test_form_with_valid_input_add_to_existing_glossary(self):
        self.assertTrue(self.valid_form_with_existing_glossary.is_bound)
        self.assertTrue(self.valid_form_with_existing_glossary.is_valid())
        self.assertEqual(self.valid_form_with_existing_glossary.errors, {})
        self.assertEqual(self.valid_form_with_existing_glossary.errors.as_text(), "")
        self.assertEqual(self.valid_form_with_existing_glossary.cleaned_data["existing_glossary"], self.glossary_obj)
        self.assertEqual(self.valid_form_with_existing_glossary.cleaned_data["title"], "")
        self.assertEqual(self.valid_form_with_existing_glossary.cleaned_data["notes"], "Some test notes.")
        self.assertEqual(self.valid_form_with_existing_glossary.cleaned_data["glossary_file"].name, "test_glossary_file.txt")

    def test_form_with_valid_input_create_new_glossary(self):
        pass

    # Test empty form
    """
    def test_form_with_no_input(self):
        self.assertFalse(self.empty_form.is_bound)
        self.assertFalse(self.empty_form.is_valid())
        with self.assertRaises(AttributeError):
            self.empty_form.cleaned_data
    """
    # Test validation edge cases
    """
    def test_form_with_invalid_input_blank_title(self):
        self.assertFalse(self.invalid_form_1.is_valid())
        self.assertNotEqual(self.invalid_form_1.errors, {})
        self.assertEqual(self.invalid_form_1.errors["title"], ["このフィールドは入力必須です。"])

    def test_form_with_invalid_input_title_too_long(self):
        self.assertFalse(self.invalid_form_2.is_valid())
        self.assertNotEqual(self.invalid_form_2.errors, {})
        self.assertEqual(self.invalid_form_2.errors["title"], ["100文字以下になるように変更してください。"])
    """
