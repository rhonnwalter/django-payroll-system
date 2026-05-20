from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Employee

class EmployeeTests(TestCase):
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
                'department': 'HR',
                'employee_type': 'FULLTIME',
                'pay_type': 'salary',
                'hourly_rate': 0,
                'salary_per_period': 50000,
        }

        response = self.client.post(url, data)

      

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Employee.objects.filter(employee_id='EMP001').exists())
        employee = Employee.objects.get(employee_id='EMP001')
        self.assertEqual(employee.user.username, 'spongebob')