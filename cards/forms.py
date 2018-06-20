from django import forms
from django.forms import formset_factory


class AddCardForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )


class AnswerOptionForm(forms.Form):
    option = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control col-10 m-auto'}),
    )


AnswerOptionsFormSet = formset_factory(AnswerOptionForm)
