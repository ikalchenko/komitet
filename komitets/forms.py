from django import forms


class CreateKomitetForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', }))


class InviteUserToKomitetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', })
    )


InviteUserFormSet = forms.formset_factory(InviteUserToKomitetForm, extra=2)
