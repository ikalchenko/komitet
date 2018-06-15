from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'komitets'
urlpatterns = [
    path('', login_required(views.MainView.as_view()), name='main'),
    path('<int:pk>', login_required(views.KomitetDetailView.as_view()), name='komitet-detail'),
    path('new-komitet', login_required(views.CreateKomitetView.as_view()), name='create-komitet'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
