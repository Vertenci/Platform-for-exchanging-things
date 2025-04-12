from django.forms import ModelForm
from django import forms
from .models import Ad, ExchangeProposal


class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите описание'}),
            'image_url': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите категорию'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }


class ExchangeProposalForm(ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']
        widgets = {
            'ad_sender': forms.Select(attrs={'class': 'form-control mb-3'}),
            'comment': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 5, 'placeholder': 'Введите комментарий...'}),
        }
        labels = {
            'ad_sender': 'Выберите ваше объявление',
            'comment': 'Комментарий',
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
