from django import forms


class CreateKomitetForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', }))
