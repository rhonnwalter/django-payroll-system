from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import User
from tasks.models import Employee

def get_base_employee():
    return Employee.objects.select_related('user').filter(is_active=True)


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


@transaction.atomic
def create_employee_service(form):
    if not form.is_valid():
        raise ValueError("Invalid form data")
    
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    if User.objects.filter(username=username).exists():
        raise ValueError("Username already exists")
    
    user = User.objects.create_user(
                username=username,
                password=password
    )
    employee = form.save(commit=False)
    employee.user = user
    employee.save()
    
    return employee

    
    
   