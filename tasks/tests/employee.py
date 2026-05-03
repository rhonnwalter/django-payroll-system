from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from models import Employee

class EmployeeTests(APITestCase):
    def setUp(self):
        self.hr_user = User.objects.create_user(
            username='jasonHR', password='titom123', is_staff=True
        )
        self.client.login(username='jasonHR', password='titom123')

    def test_get_create_employee(self):
        url = reverse('create_employee')
        data = {
                'username': 'spongebob',
                'password': '1234',
                'employee_id': 'EMP001',
                'position': 'Head',
                'department': 'hr',
                'employee_type': 'Fulltime',
                'pay_type': 'Monthly',
                'hourly_rate': 0,
                'salary_rate': 50000,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Employee.objects.filter(employee_id='EMP001').exists())
        employee = Employee.objects.get(employee_id='EMP001')
        self.assertEqual(employee.user.username, 'spongebob')