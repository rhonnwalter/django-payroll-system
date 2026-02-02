from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Employee, Payroll


@login_required
def dashboard(request):
    return render(request,  "dashboard.html")
# Create your views here.
def employee_list(request):
    employees = Employee.objects.all()
    return render (request, 'tasks/employee_list.html', {'employees':employees})

def payroll_list(request):
    payrolls = Payroll.objects.select_related('employee').all() #queryset fetched Payrolls and related attributes of the foreign key on 'employee'
    return render (request, 'tasks/payroll_list.html', {'payrolls':payrolls})

def payroll_detail(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    return render (request, 'tasks/payroll_detail.html', {'payroll': payroll})