from django import forms
from django.core.validators import FileExtensionValidator

from ..models import Glossary


class GlossaryCreateForm(forms.ModelForm):
    title = forms.CharField(
        label='用語集のタイトル',
        error_messages={
            "required": "このフィールドは入力必須です。",
        },
    )
    notes = forms.CharField(
        label='備考（任意）',
        required=False,
        widget=forms.Textarea(attrs={'rows': 6}),
    )

    class Meta:
        model = Glossary
        fields = ('title', 'notes')


class GlossaryUpdateForm(forms.ModelForm):
    title = forms.CharField(
        label='用語集のタイトル',
        error_messages={
            "required": "このフィールドは入力必須です。",
        },
    )
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False
    )

    class Meta:
        model = Glossary
        fields = ('title', 'notes')


class GlossaryUploadForm(forms.ModelForm):
    glossary_file = forms.FileField(
        label="ファイルを選択してください。",
        error_messages={"required": "このフィールドは入力必須です。"},
        validators=[
            FileExtensionValidator(
                allowed_extensions=["txt"],
                message=['拡張子が".txt "のファイルを選択してください。'],
            )
        ],
    )
    title = forms.CharField(
        label='新しい用語集のタイトル',
        error_messages={"required": "このフィールドは入力必須です。"},
    )
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False
    )

    class Meta:
        model = Glossary
        fields = ("glossary_file", "title", "notes")

    def clean(self):
        """ Check to prevent using a glossary name that already exists. """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title:
            if Glossary.objects.filter(title__iexact=title).exists():
                msg = 'このタイトルの用語集はすでに存在しています。'
                self.add_error('title', msg)


"""
class GlossaryExportForm(forms.ModelForm):
    glossaries = forms.ModelMultipleChoiceField(
        queryset=Glossary.objects.all(),
        label='Select glossaries to be exported',
        required=True,
        widget=forms.SelectMultiple(attrs={'size': 20}),
        error_messages={
            "required": "Please select at least one glossary.",
        },
    )

    class Meta:
        model = Glossary
        fields = ('glossaries',)
"""
