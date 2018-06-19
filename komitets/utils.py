from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_invitation_email(request, to_emails, pk):
    current_site = get_current_site(request)
    mail_subject = 'You have been invited to Komitet'
    message = render_to_string('komitets/invitation_email.html', {
        'user': request.user,
        'domain': current_site.domain,
        'pk': pk,
    })
    email = EmailMessage(mail_subject, message, to=to_emails)
    email.send()
