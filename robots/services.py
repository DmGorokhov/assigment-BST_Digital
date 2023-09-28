import json
from pydantic import BaseModel, constr, ValidationError
from datetime import datetime
from .models import Robot
from django.http import HttpResponseServerError
from django.db import DatabaseError


class BaseRobotData(BaseModel):
    model: constr(max_length=2)
    version: constr(max_length=2)
    created: datetime


class NewRobot(BaseRobotData):
    serial: constr(max_length=5)


class NewRobotResponse(BaseModel):
    data: dict = None
    error: list = None


def create_new_robot(request_data: json) -> NewRobotResponse:
    try:
        parsed_data = BaseRobotData.model_validate_json(request_data)
        new_robot_serial = f'{parsed_data.model}-{parsed_data.version}'
        new_robot = NewRobot(**parsed_data.model_dump(),
                             serial=new_robot_serial)
        return NewRobotResponse(data=new_robot.model_dump())
    except ValidationError as er:
        return NewRobotResponse(error=er.errors())


def save_new_robot(new_robot_data):
    try:
        new_robot = Robot.objects.create(**new_robot_data)
        return new_robot
    except DatabaseError:
        response_data = {'error_message': "Internal Server Error"}
        return HttpResponseServerError(json.dumps(response_data),
                                       content_type='application/json')
