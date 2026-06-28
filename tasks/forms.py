from django import forms
from .models import Attendance
from .models import Employee
import datetime


class AttendanceForm(forms.ModelForm):

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date', 'value': datetime.date.today()}),
        label="Date"

    )
    class Meta:
       model = Attendance
       fields = ['employee', 'date','regular_hours', 'overtime_hours']
class GeneratePayrollForm(forms.Form):
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
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete':'off'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete':'off'})
    )
    
   
    class Meta:  
        model = Employee
        fields = [   
                'employee_id',
                'position',
                'department',
                'employee_type',
                'pay_type',
                'hourly_rate',
                'salary_per_period',
               
         ]
    
    