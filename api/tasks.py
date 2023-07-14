import datetime
from django.conf import settings

import pytz
from celery import shared_task
from .models import Participant
from django.core.mail import send_mail
from django.db.models import Q

from api_for_courses.settings import TIME_ZONE


@shared_task
def remind_about_event():
    tz = new_func()
    today = datetime.datetime.now(tz=tz)
    today = today.fromtimestamp(today.timestamp()-3600)
    participants = Participant.objects.filter(
        Q(send_notification=False, course_name__start_date__lt=today)
    ).select_related('user')
    for participant in participants:
        send_mail(
            subject='Event reminder',
            from_email=settings.EMAIL_FOR_AUTH_LETTERS,
            recipient_list=[participant.user.email],
            message=f'Напоминание.\n'
                    f'В {participant.course_name.start_date}\n'
                    f'У Вас начнется курс: {participant.course_name}.',
        )
        participant.send_notification = True
        participant.save()


def new_func():
    tz = pytz.timezone(TIME_ZONE)
    return tz
