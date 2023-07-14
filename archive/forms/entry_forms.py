from django import forms

from ..models import Entry, Glossary


class EntryForm(forms.ModelForm):
    source = forms.CharField(
        label="① 原文",
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        },
    )
    target = forms.CharField(
        label="② 訳文",
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        },
    )
    glossary = forms.ModelChoiceField(
        label="③ 既存の用語集に関連付けますか？",
        queryset=Glossary.objects.all().order_by("title"),
        required=False,
    )
    new_glossary = forms.CharField(
        label="④ または、この用語のために新しい用語集を作成しますか？",
        widget=forms.TextInput(attrs={"placeholder": "新しい用語集のタイトルを入力してください。"}),
        required=False,
    )
    notes = forms.CharField(
        label="⑤ 備考（任意）",
        widget=forms.Textarea(attrs={"rows": 6}),
        required=False,
    )

    class Meta:
        model = Entry
        fields = ("source", "target", "glossary", "new_glossary", "notes")

    def clean(self):
        """
        Overwritten to handle validation for both glossary fields.
        Only one of the glossary fields should be filled in.
        Also handles case where new glossary is to be created for the new term.
        """

        cleaned_data = super().clean()
        existing_glossary = cleaned_data.get("glossary")
        new_glossary = cleaned_data.get("new_glossary")

        # First check the length of new_glossary, then check other aspects.
        # This avoids numerous error messages being displayed for the same
        # field at the same time, which is a bit nicer for the user.

        if len(new_glossary) > 100:
            self.add_error("new_glossary", "100文字以下になるように変更してください。")
        else:
            # If both fields have been entered, output error
            if existing_glossary and new_glossary:
                msg = "③または④のいずれかを選択してください。"
                self.add_error("glossary", msg)
                self.add_error("new_glossary", msg)

            # If neither of the fields have been entered, output error
            if not existing_glossary and not new_glossary:
                msg = "③または④のいずれかを選択してください。"
                self.add_error("glossary", msg)
                self.add_error("new_glossary", msg)

            # If new term is to be added to a new glossary
            if new_glossary and not existing_glossary:
                # If input title for new glossary already exists, output error
                if Glossary.objects.filter(title__iexact=new_glossary).exists():
                    msg = "このタイトルの用語集はすでに存在しています。"
                    self.add_error("new_glossary", msg)

        return cleaned_data


class EntryAddToGlossaryForm(forms.ModelForm):
    source = forms.CharField(
        label="① 原文",
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        },
    )
    target = forms.CharField(
        label="② 訳文",
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        },
    )
    notes = forms.CharField(
        label="③ 備考（任意）",
        widget=forms.Textarea(attrs={"rows": 6}),
        required=False,
    )

    class Meta:
        model = Entry
        fields = ("source", "target", "notes")
