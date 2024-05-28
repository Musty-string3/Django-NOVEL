from django import forms

from .models import *

class NovelForm(forms.ModelForm):
    """小説モデルのフォーム"""
    class Meta:
        model = Novel   # !利用するモデル
        fields = ('title', 'is_public') # !利用するフィールド
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'タイトルを入力',
                'class': 'form-control',
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }