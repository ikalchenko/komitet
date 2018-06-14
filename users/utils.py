from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import password_reset_token, account_activation_token


def send_confirmation_email(request, user, to_email, reset_password=None):
    current_site = get_current_site(request)
    if reset_password:
        message = render_to_string('users/password_reset_email.html', {
            'user': user, 'domain': current_site.domain,
            'uid': str(urlsafe_base64_encode(force_bytes(user.pk)),
                       encoding='utf-8'),
            'token': password_reset_token.make_token(user),
        })
        mail_subject = 'Reset password for your Komitet account.'
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    else:
        message = render_to_string('users/account_activation_email.html', {
            'user': user, 'domain': current_site.domain,
            'uid': str(urlsafe_base64_encode(force_bytes(user.pk)),
                       encoding='utf-8'),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Activate your Komitet account.'
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
