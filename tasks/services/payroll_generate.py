from django.db.models import Q, Sum
from datetime import datetime
from decimal import Decimal
from tasks.models import Employee, Attendance, Payroll
from .payroll_calculations import compute_total_pay, compute_netpay

def get_employee_work_data(employee, start_date, end_date):
    if not employee.pay_type == "hourly":
        return Decimal("0.00"), Decimal ("0.00")

    attendance_records = Attendance.objects.filter(
    employee=employee,
    date__range=[start_date, end_date]
    )

    totals = attendance_records.aggregate(
    total_regular=Sum('regular_hours'),
    total_overtime=Sum('overtime_hours')
    )

    total_regular=totals['total_regular'] or Decimal("0.00")
    total_overtime=totals['total_overtime'] or Decimal("0.00")
    
    
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