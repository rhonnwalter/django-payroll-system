from django import forms
from .models import Payroll

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee',
            'hours_worked',
            'overtime_hours',
            'total_pay'
            
        ]