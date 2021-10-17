from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.utils.log import get_task_logger

from film.models import Film
from my_imdb import settings
from user.models import CustomUser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_imdb.settings')

app = Celery('send_mail')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = get_task_logger(__name__)



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # send email every 24 hours
    sender.add_periodic_task(24, send_mail_user.s(), name='add every 24')

from django.core.mail import send_mail

@app.task
def send_mail_user():
    films = Film.objects.all().order_by('pub_date')[:10]
    users = CustomUser.objects.all()
    messages = [film.name for film in films]
    message = """{}""".format("\n".join(messages[1:]))
    for user in users:
        send_mail(
            'Our New Films',
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

