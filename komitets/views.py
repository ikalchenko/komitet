from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .forms import CreateKomitetForm
from .models import Committee


class MainView(generic.ListView):
    template_name = 'komitets/base.html'
    model = Committee
    context_object_name = 'komitets'


class KomitetDetailView(generic.DetailView):
    template_name = 'komitets/komitet_detail.html'
    model = Committee
    context_object_name = 'komitet'

    def get_context_data(self, **kwargs):
        qs = super().get_context_data()
        qs['komitets'] = Committee.objects.all()
        return qs


class CreateKomitetView(generic.FormView, ):
    template_name = 'komitets/create_komitet.html'
    form_class = CreateKomitetForm

    def form_valid(self, form):
        komitet = Committee(name=form.cleaned_data['name'])
        komitet.save()
        komitet.refresh_from_db()
        return HttpResponseRedirect(reverse('komitets:komitet-detail', kwargs={'pk': komitet.id}))

    def get_context_data(self, **kwargs):
        qs = super().get_context_data()
        qs['komitets'] = Committee.objects.all()
        return qs
