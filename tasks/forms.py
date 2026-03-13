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

class GeneratePayrollForm(forms.Modelform):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'}),
        label="Payroll_Start_Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Payroll_End_date"
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
            
        if start and end and start > end:
            raise forms.ValidationError("Start date cannot be after the end date")
        
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