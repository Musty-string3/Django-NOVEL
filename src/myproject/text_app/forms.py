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


class SentenceForm(forms.ModelForm):
    """文章モデルのフォーム"""
    class Meta():
        model = Sentence
        fields = {'text', }
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'テキストを入力',
                'class': 'form-control',
            }),
        }


class CharacterIconWidget(forms.widgets.RadioSelect):
    """アイコンを表示させるためのhtml"""
    template_name = 'widgets/character_icon_widget.html'

class CharacterChoiceField(forms.ModelChoiceField):
    """選択肢のラベルとして表示される内容を定義"""
    def label_from_instance(self, obj):
        return obj

class CharacterForm(forms.Form):
    """キャラクターモデルのフォール"""
    character = CharacterChoiceField(
        queryset = Character.objects.all(),
        widget = CharacterIconWidget,
        empty_label = None,
        label = 'キャラクターのアイコンを選択してください',
        initial = Character.objects.first(),
    )


class CharacterCreateForm(forms.ModelForm):
    """キャラクターモデルの作成"""
    class Meta():
        model = Character
        fields = ['name', 'icon', ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '名前を入力してください',
                'class': 'form-control',
            }),
            'icon': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
        }