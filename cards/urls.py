from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'cards'
urlpatterns = [
    path(
        '<int:pk>/add-card',
        login_required(views.AddCardView.as_view()),
        name='add-card'
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
