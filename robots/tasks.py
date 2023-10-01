from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_robot_available_notifications(robot_serial, customers_wait_list):
    model, version = robot_serial.split('-')
    message_subject = f"Робот {robot_serial} теперь в наличии!"
    message = (f'Добрый день! Недавно вы интересовались нашим роботом модели '
               f'{model}, версии {version}.Этот робот теперь в наличии. Если '
               f'вам подходит этот вариант - пожалуйста, свяжитесь с нами')
    send_mail(message_subject, message, settings.EMAIL_HOST_USER,
              customers_wait_list, fail_silently=True)
