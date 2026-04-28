from datetime import datetime
from django.db.models import Q
from models import Attendance
from django.shortcuts import get_object_or_404
from .permission_services import is_hr
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

def get_attendance_detail (user, pk):
    queryset = Attendance.objects.select_related('employee__user')

    if not (is_hr(user)):
        queryset = queryset.filter(employee__user=user)
    
    return get_object_or_404(queryset, pk=pk)

def create_attendance_service(form):
    attendance  = form.save(commit=False)

    attendance.save()
    return attendance