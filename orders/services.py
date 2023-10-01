import json
from pydantic import BaseModel, constr, ValidationError, EmailStr
from django.db import DatabaseError
from customers.models import Customer
from robots.models import Robot
from .models import Order


class RequestOrder(BaseModel):
    serial: constr(max_length=5)
    customer: EmailStr


class ParsedOrder(BaseModel):
    clean_data: dict = None
    error: list = None


class NewOrderResponse:

    def __init__(self, customer, robot_serial):
        self.response_states = {
            "not_created": ({'failed': 'order not create'}, 500),
            "created": ({'success': 'order created'}, 200),
            "robot unavailable": ({'info': (f'Sorry, asking robot out of stock'
                                            f' now, we will inform you by email'
                                            f' when it become available')}, 200)
        }
        self.state = "not_created"
        self.customer = customer
        self.robot_serial = robot_serial

    def get_state(self):
        return self.state

    @property
    def response_data(self):
        return self.response_states[self.state][0]

    @property
    def response_status(self):
        return self.response_states[self.state][1]

    def create(self):
        self.state = "created"

    def robot_unavailable(self):
        self.state = "robot unavailable"

    def to_json(self):
        return {'state': self.get_state(),
                'customer': self.customer,
                'robot_serial': self.robot_serial}


def get_parsed_and_validate_order(request_data: json) -> ParsedOrder:
    try:
        order_request = RequestOrder.model_validate_json(request_data)
        return ParsedOrder(clean_data=order_request.model_dump())
    except ValidationError as er:
        return ParsedOrder(error=er.errors())


def _find_or_create_customer(email: str):
    customer, created = Customer.objects.get_or_create(email=email)
    return customer


def _find_and_take_robot(serial: str):
    robots = Robot.objects.filter(serial=serial)
    if robots.exists():
        robot = robots.first()
        robot_serial = robot.serial
        robot.delete()
        return robot_serial
    return


def _create_order(customer, robot_serial):
    return Order.objects.create(customer=customer, robot_serial=robot_serial)


def create_new_order(order_data: json):
    customer = order_data.get('customer')
    robot_serial = order_data.get('serial')
    order_response = NewOrderResponse(customer, robot_serial)
    try:
        db_customer = _find_or_create_customer(customer)
        robot_serial_in_db = _find_and_take_robot(robot_serial)
        if robot_serial_in_db:
            _create_order(db_customer, robot_serial)
            order_response.create()
        else:
            order_response.robot_unavailable()
        return order_response
    except DatabaseError:
        return order_response
