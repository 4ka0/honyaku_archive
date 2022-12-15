from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe

from .models import Entry, Glossary, Translation


class EntryCreateForm(forms.ModelForm):
    source = forms.CharField(
        label='原文',
        error_messages={
            "required": "このフィールドは入力必須です。",
        }
    )
    target = forms.CharField(
        label='訳文',
        error_messages={
            "required": "このフィールドは入力必須です。",
        }
    )
    glossary = forms.ModelChoiceField(
        label='既存の用語集に追加しますか？',
        queryset=Glossary.objects.all().order_by('title'),
        required=False
    )
    new_glossary = forms.CharField(
        label='または、この用語のために新しい用語集を作成しますか？',
        widget=forms.TextInput(attrs={'placeholder': '新しい用語集のタイトルを入力してください'}),
        required=False
    )
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False
    )

    class Meta:
        model = Entry
        fields = ('source', 'target', 'glossary', 'new_glossary', 'notes')

    def clean(self):
        """ Overwritten to handle validation for both glossary fields.
            Only one of the glossary fields should be filled in.
            Also handles case where new glossary is to be created for the new term. """
        cleaned_data = super().clean()
        existing_glossary = cleaned_data.get('glossary')
        new_glossary = cleaned_data.get('new_glossary')

        # If both fields have been entered, output error
        if existing_glossary and new_glossary:
            existing_glossary_msg = "既存の用語集を選択してください..."
            new_glossary_msg = "...または新しい用語集を作成してください。"
            self.add_error('glossary', existing_glossary_msg)
            self.add_error('new_glossary', new_glossary_msg)

        # If neither of the fields have been entered, output error
        if not (existing_glossary or new_glossary):
            existing_glossary_msg = "既存の用語集を選択してください..."
            new_glossary_msg = "...または新しい用語集を作成してください。"
            self.add_error('glossary', existing_glossary_msg)
            self.add_error('new_glossary', new_glossary_msg)

        # If new term is to be added to a new glossary
        if not existing_glossary and new_glossary:
            # If input title for new glossary already exists, output error
            if Glossary.objects.filter(title__iexact=new_glossary).exists():
                msg = 'このタイトルの用語集はすでに存在しています。'
                self.add_error('new_glossary', msg)
            else:
                # Create new Glossary instance having title from new_glossary
                create_glossary = Glossary(title=new_glossary)
                create_glossary.save()
                # Add new glossary object to form data
                # (immutable so have to use copy() here)
                cleaned_data = self.data.copy()
                cleaned_data['glossary'] = create_glossary
                return cleaned_data


class EntryUpdateForm(forms.ModelForm):
    source = forms.CharField(label='原文')
    target = forms.CharField(label='訳文')
    glossary = forms.ModelChoiceField(
        label='リソース',
        queryset=Glossary.objects.all().order_by('title'),
        empty_label=None,  # Removes the empty option "-----"
    )
    notes = forms.CharField(
        label='備考',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False
    )

    class Meta:
        model = Entry
        fields = ('source', 'target', 'glossary', 'notes')


class EntryAddToGlossaryForm(forms.ModelForm):
    source = forms.CharField(label='Source language term')
    target = forms.CharField(label='Target language term')
    notes = forms.CharField(
        label='Notes (optional)',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False
    )

    class Meta:
        model = Entry
        fields = ('source', 'target', 'notes')


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


class GlossaryCreateForm(forms.ModelForm):
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


class TranslationUpdateForm(forms.ModelForm):
    job_number = forms.CharField(
        label='案件番号',
        error_messages={
            "required": "このフィールドは入力必須です。",
        },
    )
    translator = forms.CharField(label='翻訳者（任意）')
    field = forms.CharField(label='分野（任意）')
    client = forms.CharField(label='クライアント（任意）')
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False
    )

    class Meta:
        model = Translation
        fields = ("job_number", "translator", "field", "client", "notes")


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


class TranslationUploadForm(forms.ModelForm):
    translation_file = forms.FileField(
        # mark_safe() used to include br tag in the label.
        label=mark_safe("ファイルを選択してください。<br>DOCX、TMX、XLIFFファイルのみ読み込み可能です。"),
        error_messages={
            "required": "このフィールドは入力必須です。",
        },
        validators=[
            FileExtensionValidator(
                allowed_extensions=["docx", "tmx", "xlf"],
                message=['拡張子が .docx、.tmx、.xlf"のファイルをお選びください。'],
            )
        ],
    )
    job_number = forms.CharField(
        label='案件番号',
        error_messages={"required": "このフィールドは入力必須です。"}
    )
    translator = forms.CharField(label='翻訳者（任意）', required=False)
    field = forms.CharField(label='分野（任意）', required=False)
    client = forms.CharField(label='クライアント（任意）', required=False)
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False
    )

    class Meta:
        model = Translation
        fields = ('translation_file', 'job_number', 'translator', 'field', 'client', 'notes')

    def clean(self):
        cleaned_data = super().clean()

        # Check to prevent assigning a job number that already exists.
        job_number = cleaned_data.get('job_number')
        if job_number:
            if Translation.objects.filter(job_number__iexact=job_number).exists():
                msg = 'その案件番号の翻訳はすでに存在しています。'
                self.add_error('job_number', msg)

        # Check that only one file type has been selected.
        file_type = cleaned_data.get('file_type')
        if file_type and len(file_type) > 1:
            msg = 'ファイルの種類を1つのみ選択してください。'
            self.add_error('file_type', msg)
