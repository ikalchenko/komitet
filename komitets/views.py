from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from users.models import UserPermissions
from .utils import send_invitation_email
from .forms import CreateKomitetForm, InviteUserFormSet
from .models import Committee


class MainView(generic.ListView):
    template_name = 'komitets/app_base.html'
    context_object_name = 'komitets'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['user'] = self.request.user
        return data

    def get_queryset(self):
        return Committee.objects.filter(members__id=self.request.user.id)


class KomitetDetailView(generic.DetailView):
    template_name = 'komitets/komitet_detail.html'
    model = Committee
    context_object_name = 'komitet'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['komitets'] = Committee.objects.filter(members__id=self.request.user.id)
        data['user'] = self.request.user
        return data


class CreateKomitetView(generic.FormView):
    template_name = 'komitets/create_komitet.html'
    form_class = CreateKomitetForm

    def form_valid(self, form):
        print(form.cleaned_data)
        komitet = Committee(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            photo=self.request.FILES['photo']
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
        data['komitets'] = Committee.objects.filter(members__id=user.id)
        data['user'] = user
        return data


class AddUsersView(generic.FormView):
    template_name = 'komitets/add_users.html'
    form_class = InviteUserFormSet

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        user = self.request.user
        data['komitets'] = Committee.objects.filter(members__id=user.id)
        data['komitet'] = Committee.objects.get(pk=self.kwargs.get('pk'))
        data['user'] = user
        return data

    def form_valid(self, formset):
        emails_to_invite = []
        for data in formset.cleaned_data:
            print(data)
            try:
                user = User.objects.get(email=data['email'])
                committee = Committee.objects.get(pk=self.kwargs['pk'])
                committee.members.add(user, permission='RW')
            except User.DoesNotExist:
                emails_to_invite.append(data['email'])
        if emails_to_invite:
            send_invitation_email(self.request, emails_to_invite, self.kwargs['pk'])


