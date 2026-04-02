from django.db.models import Q
from datetime import datetime
from decimal import Decimal
from .models import Employee, Attendance, Payroll
from .payroll_calculations import compute_total_pay, compute_netpay

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

def get_employee_work_data(employee, start_date, end_date):
    if employee.pay_type == "hourly":
        attendance_records = Attendance.objects.filter(
        employee=employee,
        date__range=[start_date, end_date]
        )
        total_regular = Decimal(sum(a.regular_hours for a in attendance_records))
        total_overtime = Decimal(sum(a.overtime_hours for a in attendance_records))
    
    else:
        total_regular = 0
        total_overtime = 0
    
    return total_regular, total_overtime

def build_payroll_data(employee, start_date, end_date, total_regular, total_overtime): 
    gross_pay = compute_total_pay(employee, total_regular, total_overtime)
    net_pay, deductions = compute_netpay(gross_pay)

    return {
        "employee": employee,
        "payroll_period_start": start_date,
        "payroll_period_end": end_date,
        "gross_pay": gross_pay,
        "net_pay": net_pay,
        "sss": deductions["sss"],
        "philhealth": deductions["philhealth"],
        "tax": deductions["tax"],
        "total_regular_hours": total_regular,
        "total_overtime_hours": total_overtime
    }

def generate_payroll(start_date, end_date):
    employees = Employee.objects.filter(is_active=True)
    payroll_objects = []

    for employee in employees:

        if Payroll.objects.filter(
            employee=employee,
            payroll_period_start=start_date,
            payroll_period_end=end_date
        ).exists():
            continue

        total_regular, total_overtime = get_employee_work_data(
            employee, start_date, end_date
        )
        
        payroll_data = build_payroll_data(
            employee, start_date, end_date, 
            total_regular, total_overtime 
        )

        payroll_objects.append(Payroll(**payroll_data))
    
    Payroll.objects.bulk_create(payroll_objects)

    return len(payroll_objects)
