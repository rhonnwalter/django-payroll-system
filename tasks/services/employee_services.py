from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import redirect
from forms import EmployeeForm
def filter_employees(queryset, search=None):
    if search:
        search_condition = (
            Q(user__username__icontains=search) | 
            Q(user__first_name__icontains=search) | 
            Q(user__last_name__icontains=search) | 
            Q(employee_id__icontains=search) |
            Q(position__icontains=search) |
            Q(department__icontains=search) |
            Q(employee_type__icontains=search) |
            Q(pay_type__icontains=search)
        )
        queryset = queryset.filter(search_condition)
    return queryset

def create_employee_service(form):
    
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    user = User.objects.create_user(
                username=username,
                password=password
    )
    employee = form.save(commit=False)
    employee.user = user
    employee.save()
    
    return employee