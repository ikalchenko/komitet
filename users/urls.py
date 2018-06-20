from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'users'
urlpatterns = [
    path('login',
         views.LogInView.as_view(),
         name='login'),
    path('logout',
         views.LogOutView.as_view(),
         name='logout'),
    path('signup',
         views.SignUpView.as_view(),
         name='signup'),
    path('activate/<str:uidb64>/<str:token>',
         views.ActivateUserView.as_view(),
         name='activate'),
    path('reset-password',
         views.ResetPasswordRequestView.as_view(),
         name='reset-password-request'),
    path('reset-password/<str:uidb64>/<str:token>',
         views.ResetPasswordView.as_view(),
         name='reset-password'),
    path('user/<int:pk>',
         login_required(views.UserDetailView.as_view()),
         name='user-detail'),
    path('user/<int:pk>/edit',
         login_required(views.EditUserView.as_view()),
         name='user-edit')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
