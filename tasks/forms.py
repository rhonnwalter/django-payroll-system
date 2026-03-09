from django import forms
from .models import Payroll
from .models import Employee

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee',
            'hours_worked',
            'overtime_hours',
        ]
            
class EmployeeForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:  
        model = Employee
        fields = [   
                'employee_id',
                'position',
                'hourly_rate'
         ]