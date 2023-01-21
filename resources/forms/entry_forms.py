from django import forms

from ..models import Entry, Glossary


class EntryCreateForm(forms.ModelForm):
    source = forms.CharField(
        label='原文',
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        }
    )
    target = forms.CharField(
        label='訳文',
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        }
    )
    glossary = forms.ModelChoiceField(  # change to existing_glossary
        label='既存の用語集に追加しますか？',
        queryset=Glossary.objects.all().order_by('title'),
        required=False,
    )
    new_glossary = forms.CharField(
        label='または、この用語のために新しい用語集を作成しますか？',
        widget=forms.TextInput(attrs={'placeholder': '新しい用語集のタイトルを入力してください'}),
        required=False,
    )
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
    )

    class Meta:
        model = Entry
        fields = ('source', 'target', 'glossary', 'new_glossary', 'notes')

    def clean(self):
        """
        Overwritten to handle validation for both glossary fields.
        Only one of the glossary fields should be filled in.
        Also handles case where new glossary is to be created for the new term.
        """

        cleaned_data = super().clean()
        existing_glossary = cleaned_data.get('glossary')
        new_glossary = cleaned_data.get('new_glossary')

        # First check the length of new_glossary, then check other aspects.
        # This avoids numerous error messages being displayed for the same
        # field at the same time, which is a bit nicer for the user.
        if len(new_glossary) > 100:
            self.add_error('new_glossary', '100文字以下になるように変更してください。')
        else:

            # If both fields have been entered, output error
            if existing_glossary and new_glossary:
                existing_glossary_msg = "既存の用語集を選択してください..."
                new_glossary_msg = "...または新しい用語集を作成してください。"
                self.add_error('glossary', existing_glossary_msg)
                self.add_error('new_glossary', new_glossary_msg)

            # If neither of the fields have been entered, output error
            if not existing_glossary and not new_glossary:
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
                    newly_created_glossary = Glossary(title=new_glossary)
                    newly_created_glossary.save()
                    # Add new glossary object to form data
                    # (immutable so have to use copy() here)
                    cleaned_data = self.data.copy()
                    cleaned_data['glossary'] = newly_created_glossary

        return cleaned_data


class EntryUpdateForm(forms.ModelForm):
    source = forms.CharField(
        label='原文',
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        }
    )
    target = forms.CharField(
        label='訳文',
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        }
    )
    glossary = forms.ModelChoiceField(
        label='リソース',
        queryset=Glossary.objects.all().order_by('title'),
        empty_label=None,  # Removes the empty option "-----"
    )
    notes = forms.CharField(
        label='備考',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
    )

    class Meta:
        model = Entry
        fields = ('source', 'target', 'glossary', 'notes')


class EntryAddToGlossaryForm(forms.ModelForm):
    source = forms.CharField(
        label='原文',
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        }
    )
    target = forms.CharField(
        label='訳文',
        error_messages={
            "required": "このフィールドは入力必須です。",
            "max_length": "255文字以下になるように変更してください。",
        }
    )
    notes = forms.CharField(
        label='備考（任意）',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
    )

    class Meta:
        model = Entry
        fields = ('source', 'target', 'notes')
