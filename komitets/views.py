from django.views import generic


class TestView(generic.TemplateView):
    template_name = 'komitets/base.html'
