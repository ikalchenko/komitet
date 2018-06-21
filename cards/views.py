from django.core.exceptions import PermissionDenied
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from . import forms
from .models import Committee, Card, AnswerOption


class AddCardView(generic.FormView):
    template_name = 'cards/add_card.html'
    form_class = forms.AddCardForm

    def get_context_data(self, **kwargs):
        committee = Committee.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user in committee.get_writers():
            data = super().get_context_data()
            data['type'] = self.request.GET['type']
            user = self.request.user
            data['komitets'] = Committee.objects.committees(user=user)
            data['komitet'] = committee
            data['user'] = user
            data['users'] = committee.get_not_banned()
            data['admins'] = committee.get_admins()
            if self.request.GET['type'] == 'MOPOLL' \
                or self.request.GET['type'] == 'MAPOLL':
                data['formset'] = forms.AnswerOptionsFormSet()
            return data
        raise PermissionDenied

    def form_valid(self, form):
        committee = Committee.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        card = Card.objects.create(
            committee=committee,
            title=form.cleaned_data['title'],
            text=form.cleaned_data['text'],
            type=self.request.GET['type'],
            user=user,
        )
        card.refresh_from_db()
        if 'form-TOTAL_FORMS' in self.request.POST:
            formset = forms.AnswerOptionsFormSet(self.request.POST)
            if formset.is_valid():
                objs_to_create = list()
                for frm in formset.forms:
                    objs_to_create.append(AnswerOption(
                        card=card,
                        answer_content=frm.cleaned_data['option'], )
                    )
                answer_options = AnswerOption.objects.bulk_create(
                    objs_to_create
                )
                return HttpResponseRedirect(
                    reverse('komitets:komitet-detail',
                            kwargs={'pk': self.kwargs['pk']})
                )
            return ValidationError('Invalid options')
        if card.type == 'YNPOLL':
            answer_options = AnswerOption.objects.bulk_create((
                AnswerOption(
                    card=card,
                    answer_content='yes'),
                AnswerOption(
                    card=card,
                    answer_content='no'),
            ))
        return HttpResponseRedirect(
            reverse('komitets:komitet-detail',
                    kwargs={'pk': self.kwargs['pk']})
        )
