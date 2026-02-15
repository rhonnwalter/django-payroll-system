from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from datetime import date


# MODELS
def validate_half_hour(value): #validator for decimal .50 in hours_worked and overtime_hours
    if (value * 100) % 50 != 0: 
        raise ValidationError('Hours must be in increments of 0.50') 
    

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    position  =models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    is_active = models.BooleanField(default = True)
    date_hired = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.username}"
    
class Payroll(models.Model):
    employee = models.ForeignKey(Employee ,on_delete=models.CASCADE)
    payroll_period = models.DateField(default=date.today)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    hours_worked = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[validate_half_hour]
        ) #validators validates the input if applicable to decimal .50
    
    overtime_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        validators=[validate_half_hour]
        ) 
    
    
    def total_pay(self):
        overtime_rate = self.employee.hourly_rate * Decimal ('1.25') 
        total = (
            self.hours_worked * self.employee.hourly_rate + 
            self.overtime_hours * overtime_rate

        )
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) #sets the precision as 2. decimal places.
    
    class Meta:
        unique_together = ('employee', 'payroll_period')
        ordering = ['-payroll_period']
    


    def __str__(self):
        return f"Payroll - {self.employee.user.username}"
  


