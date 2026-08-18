from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import User
from tasks.models import Employee, Department, Position
from django.shortcuts import get_object_or_404

def get_base_employee():
    return Employee.objects.select_related('user').filter(is_active=True)

def get_department(dept_id=None):
    return Department.objects.get(id=dept_id)

def filter_positions_by_department(dept_id=None):
    return Position.objects.filter(department_id=dept_id).values('id', 'title')



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




    
def department_list():
    return Department.objects.all()
   