from django import forms
from django.core.validators import FileExtensionValidator

from ..models import Glossary


class GlossaryForm(forms.ModelForm):
    title = forms.CharField(
        label='用語集のタイトル',
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "100文字以下になるように変更してください。",
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
    existing_glossary = forms.ModelChoiceField(
        label='既存の用語集に追加しますか？',
        queryset=Glossary.objects.all().order_by('title'),
        required=False,
    )
    new_glossary = forms.CharField(
        label='または、新しい用語集を作成しますか？',
        widget=forms.TextInput(attrs={'placeholder': '新しい用語集のタイトルを入力してください'}),
        required=False,
    )
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
    )

    class Meta:
        model = Glossary
        fields = ("glossary_file", "existing_glossary", "new_glossary", "notes")

    def clean(self):
        """
        Overriden to handle error checking for the new glossary and the existing
        glossary fields.
        """

        cleaned_data = super().clean()
        existing_glossary = cleaned_data.get('existing_glossary')
        new_glossary = cleaned_data.get('new_glossary')

        # First check the length of new_glossary, then check other aspects.
        # This avoids numerous error messages being displayed for the same
        # field at the same time, which is a bit nicer for the user.
        if len(new_glossary) > 100:
            self.add_error('new_glossary', '100文字以下になるように変更してください。')
        else:

            # If both fields have been entered, output error.
            if existing_glossary and new_glossary:
                existing_glossary_msg = "既存の用語集を選択してください..."
                new_glossary_msg = "...または新しい用語集を作成してください。"
                self.add_error('existing_glossary', existing_glossary_msg)
                self.add_error('new_glossary', new_glossary_msg)

            # If neither of the glossary fields have been entered, output error.
            if not existing_glossary and not new_glossary:
                existing_glossary_msg = "既存の用語集を選択してください..."
                new_glossary_msg = "...または新しい用語集を作成してください。"
                self.add_error('existing_glossary', existing_glossary_msg)
                self.add_error('new_glossary', new_glossary_msg)

            # If a new glossary is to be created, and the entered title for the new
            # glossary already exists, output error.
            if new_glossary and not existing_glossary:
                if Glossary.objects.filter(title__iexact=new_glossary).exists():
                    msg = 'このタイトルの用語集はすでに存在しています。'
                    self.add_error('new_glossary', msg)

        return cleaned_data


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
