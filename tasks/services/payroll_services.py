from django.db.models import Q
from models import Payroll
from django.shortcuts import get_object_or_404
from .permission_services import is_hr
def filter_payrolls(queryset, search=None):
    if search: 
        search_condition = (
            Q(employee__user__username__icontains=search) |
            Q(employee__position__icontains=search)  |
            Q(employee__department__icontains=search)  |
            Q(employee__pay_type__icontains=search)  
        )

        queryset = Payroll.filter(search_condition)

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