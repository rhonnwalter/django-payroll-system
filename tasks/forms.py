from django import forms
from .models import Attendance
from .models import Employee

class AttendanceForm(forms.ModelForm):
    class meta:
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
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:  
        model = Employee
        fields = [   
                'employee_id',
                'position',
                'department',
                'pay_type,',
                'hourly_rate',
         ]