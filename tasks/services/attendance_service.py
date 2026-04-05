from datetime import datetime
from django.db.models import Q
def filter_attendances(queryset, search=None, date_from=None, date_to=None):

    if date_from:
        try: 
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            queryset = queryset.filter(date__gte=date_from)
        except ValueError: 
            date_from = None
            
    if date_to:
        try: 
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
            queryset = queryset.filter(date__lte=date_to)
        except ValueError:
            date_to = None

    if search:
        search_condition = (
            Q(employee__user__username__icontains=search) |
            Q(employee__user__first_name__icontains=search) |
            Q(employee__user__last_name__icontains=search) |
            Q(employee__department__icontains=search) 
        )
        queryset = queryset.filter(search_condition)

    return queryset