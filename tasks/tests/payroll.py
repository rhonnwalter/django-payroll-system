from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Employee
from django.urls import reverse

class PayrollTests(TestCase):
    def setUp(self):
        self.hr_user=User.objects.create_user(
            username='rhonnHR', password='rhonn', is_staff=True
        )
        self.client.login(username='rhonnHR', password='rhonn', is_staff=True)

    def test_generate_payroll(self):
        url =  reverse('generate_payroll')
        data = {
        
        }