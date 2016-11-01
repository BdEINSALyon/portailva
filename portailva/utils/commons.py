import os

from anymail.message import attach_inline_image_file
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from premailer import transform


def send_mail(template_html_name=None, template_text_name=None, context=None, subject=None, from_email=None, to=None):
    # Plain text part
    text_content = render_to_string(template_text_name, context=context)


    if from_email is None:
        from_email = settings.PORTAILVA_APP['site']['email_noreply']

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to])

    # Making context
    logo_cid = attach_inline_image_file(msg, os.path.join(settings.BASE_DIR, "assets/img/logo_mail.png"))
    context.update({
        'logo_cid': logo_cid,
        'app': settings.PORTAILVA_APP
    })

    # HTML part
    html_content = render_to_string(template_html_name, context=context)
    inlined_html_content = transform(html_content)

    msg.attach_alternative(inlined_html_content, "text/html")
    msg.send()
