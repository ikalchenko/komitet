from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .forms import CreateKomitetForm, InviteUserFormSet
from .models import Committee
from users.models import UserPermissions


class MainView(generic.ListView):
    template_name = 'komitets/app_base.html'
    model = Committee
    context_object_name = 'komitets'

    def get_context_data(self, **kwargs):
        qs = super().get_context_data()
        qs['user'] = self.request.user
        return qs


class KomitetDetailView(generic.DetailView):
    template_name = 'komitets/komitet_detail.html'
    model = Committee
    context_object_name = 'komitet'

    def get_context_data(self, **kwargs):
        qs = super().get_context_data()
        qs['komitets'] = Committee.objects.all()
        qs['user'] = self.request.user
        return qs


class CreateKomitetView(generic.FormView):
    template_name = 'komitets/create_komitet.html'
    form_class = CreateKomitetForm

    def form_valid(self, form):
        komitet = Committee(name=form.cleaned_data['name'])
        komitet.save()
        komitet.refresh_from_db()
        permission = UserPermissions.objects.create(user=self.request.user, committee=komitet, permission='A')
        permission.save()
        return HttpResponseRedirect(reverse('komitets:komitet-detail', kwargs={'pk': komitet.id}))

    def get_context_data(self, **kwargs):
        qs = super().get_context_data()
        user = self.request.user
        qs['komitets'] = user.committee_set.all()
        qs['user'] = user
        qs['invite_form'] = InviteUserFormSet()
        return qs
