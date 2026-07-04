from django.db.models import Q
from tasks.models import Payroll
from django.shortcuts import get_object_or_404
from .permission_services import is_hr
from django.utils import timezone

def filter_payrolls(queryset, search=None, month=None, year=None):
    if search: 
        search_condition = (
            Q(employee__user__username__icontains=search) |
            Q(employee__position__icontains=search)  |
            Q(employee__department__icontains=search)  |
            Q(employee__pay_type__icontains=search)  
        )

        queryset = queryset.filter(search_condition)

    if month: 
        queryset = queryset.filter(payroll_period_start__month=month)
    if year: 
        queryset = queryset.filter(payroll_period_start__year=year)
    return queryset

def mark_payroll_paid (payroll, user=None):
    payroll.status = 'paid'
    payroll.save()
    return payroll
    
def get_payroll_detail (user, pk): 
    queryset = Payroll.objects.select_related('employee__user')
    
    if not (is_hr(user)):
        queryset = queryset.filter(employee__user=user)
    
    return get_object_or_404(queryset, pk=pk)

def get_payroll_history (user, employee_id):
    queryset = Payroll.objects.select_related('employee__user')
    if (is_hr(user)):
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id).order_by('-payroll_period_start')
        else:
            queryset = queryset.all().order_by('-payroll_period_start')
    else:
        queryset = queryset.objects.filter(
            employee__user=user
        ).order_by('payroll_period_start')

    return queryset

def get_current_month_payrolls():

    now = timezone.now()
    current_month = now.month
    current_year = now.year

    queryset = Payroll.objects.select_related('employee__user').filter(
            employee__is_active=True,
            payroll_period_start__month=current_month,
            payroll_period_start__year=current_year,
    )

    return queryset