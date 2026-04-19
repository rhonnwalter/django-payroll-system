from models import Payroll, Employee
from django.db.models import Sum

def hr_dashboard_stats():
    payrolls = Payroll.objects.annotate(total_pay_expr=Payroll.total_pay_expression())
    return {
        'payrolls' : payrolls,
        'total_employees' : Employee.objects.count(),
        'total_payrolls' : payrolls.count(),
        'total_salary' : payrolls.aggregate(Sum('total_pay_expr'))['total_pay_expr__sum'] or 0 
        #['total_pay_expr__sum' grab the actual number from the dictionary
    }
  