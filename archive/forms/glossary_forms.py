from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe

from ..models import Resource


class GlossaryForm(forms.ModelForm):
    title = forms.CharField(
        label="① 用語集のタイトル",
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "100文字以下になるように変更してください。",
        },
    )
    notes = forms.CharField(
        label="② 備考（任意）",
        required=False,
        widget=forms.Textarea(attrs={"rows": 6}),
    )

    class Meta:
        model = Resource
        fields = ("title", "notes")


class GlossaryUploadForm(forms.ModelForm):
    upload_file = forms.FileField(
        label="① ファイルを選択してください。",
        error_messages={"required": "このフィールドは入力必須です。"},
        validators=[
            FileExtensionValidator(
                allowed_extensions=["txt"],
                message=['拡張子が".txt "のファイルを選択してください。'],
            )
        ],
    )
    existing_glossary = forms.ModelChoiceField(
        label="② 既存の用語集に追加しますか？",
        queryset=Resource.objects.filter(resource_type="GLOSSARY").order_by("title"),
        required=False,
    )
    title = forms.CharField(
        label="③ または、新しい用語集を作成しますか？",
        widget=forms.TextInput(attrs={"placeholder": "新しい用語集のタイトルを入力してください。"}),
        required=False,
        error_messages={"max_length": "100文字以下になるように変更してください。"},
    )
    notes = forms.CharField(
        label="④ 備考（任意）",
        widget=forms.Textarea(attrs={"rows": 6}),
        required=False,
        help_text=mark_safe(
            ("アップロードされる用語集は既存の用語集に追加する場合、<br>" "上記の備考は既存の用語集の備考に追加されます。")
        ),
    )

    class Meta:
        model = Resource
        fields = ("upload_file", "existing_glossary", "title", "notes")

    def clean(self):
        """
        Overridden to handle error checking for the existing_glossary and the
        title fields. Only one of these should be entered. The existing_glossary
        field is used when adding upload content to an existing glossary, and the
        title field is used when creating a new glossary for the upload content.
        """

        cleaned_data = super().clean()
        existing_glossary = cleaned_data.get("existing_glossary")
        title = cleaned_data.get("title")

        # If both fields have been entered, output error.
        if existing_glossary and title:
            msg = "②または③のいずれかを選択してください。"
            self.add_error("existing_glossary", msg)
            self.add_error("title", msg)

        # If neither of the glossary fields have been entered, output error.
        if not existing_glossary and not title:
            msg = "②または③のいずれかを選択してください。"
            self.add_error("existing_glossary", msg)
            self.add_error("title", msg)

        # If a new glossary is to be created, and there is already a glossary
        # having the entered title, output error.
        if title and not existing_glossary:
            if (
                Resource.objects
                .filter(resource_type="GLOSSARY")
                .filter(title__iexact=title)
                .exists()
            ):
                msg = "このタイトルの用語集はすでに存在しています。"
                self.add_error("title", msg)

        return cleaned_data
