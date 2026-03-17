from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from datetime import date
from django.db.models import F, ExpressionWrapper, DecimalField, Case, When, Value



# MODELS
def validate_half_hour(value): #validator for decimal .50 in hours_worked and overtime_hours
    if (value * 100) % 50 != 0: 
        raise ValidationError('Hours must be in increments of 0.50') 
    

class Employee(models.Model):
    PAY_TYPE_CHOICES = [
        ("hourly", "Hourly"),
        ("salary", "Salary"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)

    position  =models.CharField(max_length=100)
    pay_type = models.CharField(max_length=10, choices=PAY_TYPE_CHOICES)

    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    salary_per_period = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overtime_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.5)
    

    is_active = models.BooleanField(default = True)
    date_hired = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.username}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()

    time_in = models.TimeField()
    time_out = models.TimeField()
    
    regular_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[validate_half_hour],
        default=0 
        )
    overtime_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_half_hour],
        default=0
    )

    
class Payroll(models.Model):
    employee = models.ForeignKey(Employee ,on_delete=models.CASCADE)

    payroll_period_start = models.DateField()
    payroll_period_end = models.DateField()

    total_regular_hours = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=validate_half_hour,
        default=0
    )
    
    total_overtime_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=validate_half_hour,
        default=0
        
    )
    
    sss = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    philhealth = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagibig = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)



    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    status_choices = (
        ('pending', 'Pending'), #first element is the actual value passed to db, second element is what is readable to admin
        ('paid', 'Paid'),
    )

    status = models.CharField(max_length=10, choices=status_choices, default='pending' )

    class Meta:
        unique_together = ('employee', 'payroll_period')
        ordering = ['-payroll_period']
    


    def __str__(self):
        return f"Payroll - {self.employee.user.username}"
  


