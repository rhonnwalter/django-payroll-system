from django.db.models import Q
from models import Payroll

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