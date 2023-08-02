from django import forms

from ..models import Item, Resource


class GlossaryItemForm(forms.ModelForm):
    """
    Form used for creating and updating Item objects that belong to glossaries.
    """
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
    resource = forms.ModelChoiceField(
        label="③ 既存の用語集に関連付けますか？",
        queryset=Resource.objects.filter(resource_type="GLOSSARY").order_by("title"),
        required=False,
    )
    new_resource = forms.CharField(
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
        model = Item
        fields = ("source", "target", "resource", "new_resource", "notes")

    def clean(self):
        """
        Overwritten to handle validation for both glossary fields.
        Only one of the glossary fields should be filled in.
        Also handles case where new glossary is to be created for the new term.
        """

        cleaned_data = super().clean()
        existing_resource = cleaned_data.get("resource")
        new_resource = cleaned_data.get("new_resource")

        # First check the length of new_resource, then check other aspects.
        # This avoids numerous error messages being displayed for the same
        # field at the same time, which is a bit nicer for the user.

        if len(new_resource) > 100:
            self.add_error("new_resource", "100文字以下になるように変更してください。")
        else:
            # If both fields have been entered, output error
            if existing_resource and new_resource:
                msg = "③または④のいずれかを選択してください。"
                self.add_error("resource", msg)
                self.add_error("new_resource", msg)

            # If neither of the fields have been entered, output error
            if not existing_resource and not new_resource:
                msg = "③または④のいずれかを選択してください。"
                self.add_error("resource", msg)
                self.add_error("new_resource", msg)

            # If new term is to be added to a new resource
            if new_resource and not existing_resource:
                # If input title for new resource already exists, output error
                if (
                    Resource.objects
                    .filter(resource_type="GLOSSARY")
                    .filter(title__iexact=new_resource)
                    .exists()
                ):
                    msg = "このタイトルの用語集はすでに存在しています。"
                    self.add_error("new_resource", msg)

        return cleaned_data


class TranslationItemForm(forms.ModelForm):
    """
    Form used for creating and updating Item objects that belong to translations.
    """
    source = forms.CharField(
        label="① 原文",
        widget=forms.Textarea(attrs={"rows": 6}),
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        },
    )
    target = forms.CharField(
        label="② 訳文",
        widget=forms.Textarea(attrs={"rows": 6}),
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        },
    )

    class Meta:
        model = Item
        fields = ("source", "target")


class GlossaryAddItemForm(forms.ModelForm):
    """
    Form used for adding an item to an existing glossary.
    """
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
        model = Item
        fields = ("source", "target", "notes")
