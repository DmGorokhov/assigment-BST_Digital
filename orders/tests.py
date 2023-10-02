from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from django.db import DatabaseError
from .models import Order


class AddNewOrderTest(TestCase):
    fixtures = ['db_robots.json']

    valid_order = {
        "serial": "R2-D2",
        "customer": "bob@mail.com"}

    invalid_order = {
        "serial": "Invalid",
        "customer": "bob@mail.com"}

    robot_not_in_db = {"serial": "X5-07",
                       "customer": "bob@mail.com"}

    def test_add_new_order(self):
        response = self.client.post(reverse('orders:new_order'),
                                    self.valid_order,
                                    content_type="application/json")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'success': 'order created'})

        orders = Order.objects.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].robot_serial, self.valid_order['serial'])
        self.assertEqual(str(orders[0].customer), self.valid_order['customer'])

    def test_robot_unavalible(self):
        response = self.client.post(reverse('orders:new_order'),
                                    self.robot_not_in_db,
                                    content_type="application/json")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'info': 'Sorry, asking robot out of stock \
                                            now, we will inform you by email \
                                            when it become available'}
                             )

    def test_invalid_order(self):
        response = self.client.post(reverse('orders:new_order'),
                                    self.invalid_order,
                                    content_type="application/json")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

    def test_add_new_order_database_error(self):
        Order.objects.create = self._raise_db_error

        response = self.client.post(reverse('orders:new_order'),
                                    self.valid_order,
                                    content_type="application/json")

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'failed': 'order not create'})

    def _raise_db_error(self, **kwargs):
        raise DatabaseError()
