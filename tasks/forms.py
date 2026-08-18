from django import forms
from .models import Attendance, Employee, User
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

class UserForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput, required=False)
        model = User
        fields = [
            'username',
            'password'
        ]
        labels = {
            'username' : 'Username',
            'password' : 'Password'
        }
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)

        if user:
            user.set_password (self.cleaned_data['password'])
            if commit: 
                user.save()
            return user



class EmployeeForm(forms.ModelForm):
   
    class Meta:  
        model = Employee
        fields = [  
                'profile_picture' ,
                'first_name',
                'middle_name',
                'last_name',
                'department',
                'position',
                'employee_type',
                'pay_type',
                'hourly_rate',
                'salary_per_period',
               
        ]
        exclude = ['employee_id']


        labels = {
            'profile_picture': 'Profile Picture',
            'first_name' : 'First Name',
            'middle_name' : 'Middle Name',
            'last_name' : 'Last Name',
            'position': 'Job Position',
            'department': 'Department Name',
            'employee_type': 'Employment Type',
            'pay_type': 'Payment Type',
            'hourly_rate': 'Hourly Rate ',
            'salary_per_period': 'Monthly Salary',
        }
  
    def save(self, commit=True):
        employee = super().save(commit=commit)
            
        return employee