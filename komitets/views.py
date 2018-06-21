from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from cards.models import Card, AnswerOption, Answer
from users.models import UserPermissions
from .forms import CreateKomitetForm, InviteUserFormSet
from .models import Committee
from .utils import send_invitation_email


class MainView(generic.ListView):
    template_name = 'komitets/app_base.html'
    context_object_name = 'komitets'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['user'] = self.request.user
        return data

    def get_queryset(self):
        return Committee.objects.committees(user=self.request.user)


class KomitetDetailView(generic.DetailView):
    template_name = 'komitets/komitet_detail.html'
    model = Committee
    context_object_name = 'komitet'

    def get_context_data(self, **kwargs):
        if self.request.user in self.object.get_not_banned():
            data = super().get_context_data()
            data['komitets'] = Committee.objects.committees(
                user=self.request.user
            )
            cards = Card.objects.filter(committee=self.object)
            data['users'] = self.object.get_not_banned()
            data['user'] = self.request.user
            data['admins'] = self.object.get_admins()
            data['writers'] = self.object.get_writers()
            data['cards'] = cards
            data['options'] = AnswerOption.objects.filter(card__in=cards)
            return data
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        post = dict(request.POST)
        del post['csrfmiddlewaretoken']
        if 'user-management' in post:
            del post['user-management']
            for key, value in post.items():
                user = User.objects.get(pk=int(key))
                committee = Committee.objects.get(pk=self.kwargs['pk'])
                user.set_permission(committee, value[0])
                return HttpResponseRedirect(reverse(
                    'komitets:komitet-detail',
                    kwargs={'pk': kwargs['pk']}
                ))
        answers_to_save = []
        key_to_delete = ''
        for key, value in post.items():
            card = Card.objects.get(pk=int(key))
            if card.type == 'YNPOLL':
                option = AnswerOption.objects.get(
                    card=card,
                    answer_content=value[0]
                )
                key_to_delete = key
                answers_to_save.append(
                    Answer(answer_option=option,
                           user=self.request.user)
                )
        if key_to_delete:
            del post[key_to_delete]
        answers_to_save.extend(
            [Answer(answer_option=AnswerOption.objects.get(pk=option_id),
                    user=self.request.user)
             for _, value in post.items()
             for option_id in value]
        )
        Answer.objects.bulk_create(answers_to_save)
        return HttpResponseRedirect(reverse(
            'komitets:komitet-detail',
            kwargs={'pk': kwargs['pk']}
        ))


class CreateKomitetView(generic.FormView):
    template_name = 'komitets/create_komitet.html'
    form_class = CreateKomitetForm

    def form_valid(self, form):
        image = self.request.FILES['image'] if 'image' in self.request.FILES \
            else None
        komitet = Committee(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            image=image
        )
        komitet.save()
        komitet.refresh_from_db()
        permission = UserPermissions.objects.create(
            user=self.request.user,
            committee=komitet,
            permission='A'
        )
        permission.save()
        return HttpResponseRedirect(
            reverse('komitets:komitet-add-users', kwargs={'pk': komitet.id})
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        user = self.request.user
        data['komitets'] = Committee.objects.committees(user=user)
        data['user'] = user
        return data


class AddUsersView(generic.FormView):
    template_name = 'komitets/add_users.html'
    form_class = InviteUserFormSet

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        user = self.request.user
        committee = Committee.objects.get(pk=self.kwargs.get('pk'))
        data['komitets'] = Committee.objects.committees(user=user)
        data['komitet'] = committee
        data['user'] = user
        data['users'] = committee.get_not_banned()
        data['admins'] = committee.get_admins()
        return data

    def form_valid(self, formset):
        committee = Committee.objects.get(pk=self.kwargs['pk'])
        if self.request.user in committee.get_not_banned():
            emails_to_invite = []
            for data in formset.cleaned_data:
                try:
                    user = User.objects.get(email=data['email'])
                    try:
                        UserPermissions.objects \
                            .get(user=user.id, committee=committee.id)
                    except UserPermissions.DoesNotExist:
                        UserPermissions.objects.create(
                            user=user,
                            committee=committee,
                            permission='RW'
                        )
                except User.DoesNotExist:
                    emails_to_invite.append(data['email'])
                except KeyError:
                    pass
            if emails_to_invite:
                send_invitation_email(
                    self.request,
                    emails_to_invite,
                    self.kwargs['pk']
                )
            return HttpResponseRedirect(reverse(
                'komitets:komitet-detail',
                kwargs={'pk': committee.id}
            ))
        raise PermissionDenied


class DeleteKomitetView(generic.DeleteView):
    model = Committee
    template_name = 'komitets/delete.html'
    success_url = reverse_lazy('komitets:main')
    context_object_name = 'komitet'

    def get_context_data(self, **kwargs):
        if self.request.user in self.object.get_admins():
            data = super().get_context_data()
            user = self.request.user
            data['komitets'] = Committee.objects.committees(user=user)
            data['user'] = user
            data['users'] = self.object.get_not_banned()
            return data
        raise PermissionDenied

