from django import forms
from .models import Attendance
from .models import Employee
from django.contrib.auth.models import User

class AttendanceForm(forms.ModelForm):
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
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
   
    class Meta:  
        model = Employee
        fields = [   
                'employee_id',
                'position',
                'department',
                'employee_type',
                'pay_type',
                'hourly_rate',
                'salary_rate',
                'date_hired'
         ]
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )

        employee = super().save(commit=False)
        employee.user = user

        if commit:
            employee.save()

        return employee 