from celery import shared_task
from R4C.utils import connect_redis


def _add_robot_to_wait_queue(robot_serial, email):
    redis_conn = connect_redis()
    redis_conn.sadd(robot_serial, email)


@shared_task
def make_post_order_tasks(order):
    match order['state']:
        case "robot unavailable":
            _add_robot_to_wait_queue(order.get('robot_serial'),
                                     order.get('customer')
                                     )
