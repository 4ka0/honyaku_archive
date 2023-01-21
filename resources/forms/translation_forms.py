from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe

from ..models import Translation


class TranslationUpdateForm(forms.ModelForm):
    job_number = forms.CharField(
        label='案件番号',
        error_messages={
            "required": "このフィールドは入力必須です。",
        },
    )
    translator = forms.CharField(label='翻訳者（任意）', required=False)
    field = forms.CharField(label='分野（任意）', required=False)
    client = forms.CharField(label='クライアント（任意）', required=False)
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
    )

    class Meta:
        model = Translation
        fields = ("job_number", "translator", "field", "client", "notes")


class TranslationUploadForm(forms.ModelForm):
    translation_file = forms.FileField(
        label="ファイルを選択してください。",
        # mark_safe() used to include br tag in the label.
        help_text=mark_safe(
            ("DOCX又はTMXファイルのみ読み込み可能です。<br>"
             "DOCXファイルの場合、日本語と英語対訳の2列からなる表のみ対象とします。")
        ),
        error_messages={
            "required": "このフィールドは入力必須です。",
        },
        validators=[
            FileExtensionValidator(
                allowed_extensions=["docx", "tmx"],
                message=['拡張子が 「.docx」又は「.tmx」のファイルをお選びください。'],
            )
        ],
    )
    job_number = forms.CharField(
        label='案件番号',
        error_messages={"required": "このフィールドは入力必須です。"},
    )
    translator = forms.CharField(label='翻訳者（任意）', required=False)
    field = forms.CharField(label='分野（任意）', required=False)
    client = forms.CharField(label='クライアント（任意）', required=False)
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
    )

    class Meta:
        model = Translation
        fields = ('translation_file', 'job_number', 'translator', 'field', 'client', 'notes')

    def clean(self):
        """
        Check to prevent assigning a job number that already exists.
        """
        cleaned_data = super().clean()
        job_number = cleaned_data.get('job_number')
        if job_number:
            if Translation.objects.filter(job_number__iexact=job_number).exists():
                msg = 'その案件番号の翻訳はすでに存在しています。'
                self.add_error('job_number', msg)
        return cleaned_data
