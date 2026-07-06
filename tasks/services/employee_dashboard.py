from tasks.models import Employee, Payroll

def employee_dashboard(user):
   return Payroll.objects.select_related('employee__user').filter(employee__user=user).order_by('-created_at')