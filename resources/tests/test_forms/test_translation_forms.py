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

    """
    job_number = forms.CharField(
        label='① 案件番号',
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "100文字以下になるように変更してください。",
        },
    )
    """

    def test_job_number_field_label(self):
        self.assertEqual(self.empty_form.fields['job_number'].label, '① 案件番号')

    def test_job_number_field_required(self):
        self.assertTrue(self.empty_form.fields["job_number"].required)

    def test_job_number_field_required_error_message(self):
        self.assertEqual(
            self.empty_form.fields['job_number'].error_messages['required'],
            'このフィールドは入力必須です。'
        )

    def test_job_number_field_max_length_error_message(self):
        self.assertEqual(
            self.empty_form.fields['job_number'].error_messages['max_length'],
            '100文字以下になるように変更してください。'
        )

    """
    field = forms.CharField(
        label='② 分野（任意）',
        required=False,
        error_messages={
            "max_length": "100文字以下になるように変更してください。",
        },
    )
    """

    """
    client = forms.CharField(
        label='③ クライアント（任意）',
        required=False,
        error_messages={
            "max_length": "100文字以下になるように変更してください。",
        },
    )
    """

    """
    translator = forms.CharField(
        label='④ 翻訳者（任意）',
        required=False,
        error_messages={
            "max_length": "100文字以下になるように変更してください。",
        },
    )
    """

    """
    notes = forms.CharField(
        label='⑤ 備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
    )
    """

    # Test Meta fields

    """
    class Meta:
        model = Translation
        fields = ("job_number", "translator", "field", "client", "notes")
    """
