from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'users'
urlpatterns = [
    path('login', views.LogInView.as_view(), name='login'),
    path('logout', views.LogOutView.as_view(), name='logout'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>', views.ActivateUserView.as_view(), name='activate'),
    path('reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
