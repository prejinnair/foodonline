from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
def detect_user(user):
    if user.role == 1:
        redirect_url = 'vendor_dashboard'
    elif user.role == 2:
        redirect_url = 'customer_dashboard'
    elif user.role == None and user.is_superadmin:
        redirect_url = '/admin'
    return redirect_url

def send_verification_email(request, user, subject, template):
    current_site = get_current_site(request)
    from_email = settings.DEFAULT_FROM_EMAIL
    mail_subject = subject
    message = render_to_string(template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, from_email, to=[to_email])
    email.send()

def send_notification(mail_subject, template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(template, context)
    to_email = context['user'].email
    email = EmailMessage(mail_subject, message, from_email, to=[to_email])
    email.send()
