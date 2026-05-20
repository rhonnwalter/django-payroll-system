from tasks.models import Payroll, Employee
from django.db.models import Sum

def hr_dashboard_stats(request):
    payrolls = Payroll.objects.all()
    return {
        'payrolls' : payrolls,
        'total_employees' : Employee.objects.count(),
        'total_payrolls' : payrolls.count(),
        'total_salary' : payrolls.aggregate(Sum('net_pay'))
        #['total_pay_expr__sum' grab the actual number from the dictionary
    }
  