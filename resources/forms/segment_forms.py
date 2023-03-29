from django import forms

from ..models import Segment


class SegmentForm(forms.ModelForm):
    source = forms.CharField(
        label='① 原文',
        widget=forms.Textarea(attrs={'rows': 6}),
        error_messages={
            "required": "このフィールドは入力必須です。",
        }

    )
    target = forms.CharField(
        label='② 訳文',
        widget=forms.Textarea(attrs={'rows': 6}),
        error_messages={
            "required": "このフィールドは入力必須です。",
        }
    )

    class Meta:
        model = Segment
        fields = ('source', 'target')
