from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Attendance, Employee
from datetime import date 

class testAttendance(TestCase):
    def setUp(self):
        self.hr_user = User.objects.create_user(
            username='jeffryHR', password='jeff', is_staff=True
        )
        self.client.login(username='jeffryHR', password='jeff')

        self.emp_user = User.objects.create_user(
            username='emp1', password='123', is_staff=False
        )

        self.employee = Employee.objects.create(
            user=self.emp_user,
            employee_id='EMP001',
            position='Head',
            department='HR',
            employee_type='FULLTIME',
            pay_type='salary',
            hourly_rate=0,
            salary_per_period=50000,
        )

    def test_create_attendance(self):
        url = reverse('create_attendance')
        data = {
            'employee': self.employee.id, 
            'date': date.today(),
            'regular_hours':8,
            'overtime_hours':2
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Attendance.objects.filter(employee=self.employee, date=date.today()).exists()                       
            )
        
        attendance = Attendance.objects.get(employee=self.employee, date=date.today())
        self.assertEqual(attendance.regular_hours, 8)
        self.assertEqual(attendance.overtime_hours, 2)
        