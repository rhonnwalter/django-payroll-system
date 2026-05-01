from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from models import Employee

class EmployeeTests(APITestCase):
    def setUp(self):
        self.hr_user = User.objects.create_user(
            username="jasonHR", password="titom123", is_staff=True
        )
        self.client.login(username="jasonHr", password="titom123")

    def test_get_create_employee(self):
        response = self.client.get(reverse("create_employee"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/create_employee.html")
        