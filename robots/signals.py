from django.db.models.signals import post_save
from django.dispatch import receiver
from robots.models import Robot
from .tasks import send_robot_available_notifications
from R4C.utils import connect_redis

redis_conn = connect_redis()


def get_customers_wait_list(robot_serial):
    return redis_conn.smembers(robot_serial)


def delete_serial(robot_serial):
    redis_conn.delete(robot_serial)


@receiver(post_save, sender=Robot)
def robot_wait_list_send_notification(sender, instance, created, **kwargs):
    if created:
        robot_serial = instance.serial
        if redis_conn.exists(robot_serial):
            customers_wait_list = list(get_customers_wait_list(robot_serial))
            send_robot_available_notifications.delay(robot_serial,
                                                     customers_wait_list)
            delete_serial(robot_serial)
