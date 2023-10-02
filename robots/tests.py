from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from django.db import DatabaseError
from .models import Robot


class AddNewRobotTest(TestCase):
    valid_robot_data = {
        "model": "R2",
        "version": "D2",
        "created": "2023-10-02T12:34:56",
        "serial": "R2-D2"
    }
    invalid_robot_data = {
        "model": "Invalid",
        "version": "1.0",
        "created": "2023-10-02T12:34:56",
        "serial": "Invalid-1.0"
    }

    def test_add_new_robot(self):
        response = self.client.post(reverse('robots:new_robot'),
                                    self.valid_robot_data,
                                    content_type="application/json")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {"success": "Robot added"})

        robots = Robot.objects.all()
        self.assertEqual(len(robots), 1)
        self.assertEqual(robots[0].model, self.valid_robot_data['model'])
        self.assertEqual(robots[0].version, self.valid_robot_data['version'])
        self.assertEqual(robots[0].serial, self.valid_robot_data['serial'])
        self.assertEqual(str(robots[0]), self.valid_robot_data['serial'])

    def test_add_new_robot_invalid_data(self):
        response = self.client.post(reverse('robots:new_robot'),
                                    self.invalid_robot_data,
                                    content_type="application/json")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        robots = Robot.objects.all()
        self.assertEqual(len(robots), 0)

    def test_add_new_robot_database_error(self):
        Robot.objects.create = self._raise_db_error

        response = self.client.post(reverse('robots:new_robot'),
                                    self.valid_robot_data,
                                    content_type="application/json")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {"error_message": "Internal Server Error"})

    def _raise_db_error(self, **kwargs):
        raise DatabaseError()
