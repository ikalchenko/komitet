from django import forms


class CreateKomitetForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', }))
    description = forms.CharField(max_length=50, widget=forms.Textarea(attrs={'class': 'form-control', }))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', }))


class InviteUserToKomitetForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control col-10 m-auto', })
    )


InviteUserFormSet = forms.formset_factory(InviteUserToKomitetForm, max_num=500)
