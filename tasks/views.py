from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
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

def payroll_detail(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        payroll = get_object_or_404 (Payroll, pk=pk)
    else:
         payroll = get_object_or_404(
    
        Payroll, #the model querying to
        pk=pk,  #looks into the payroll id that matches with the url pk
        employee__user=request.user #looks into the field employee and the user field in which is linked to the employee. 
        #and checks if those fields, matched with the user logged in.
        ) 
    return render (request, 'tasks/payroll_detail.html', {'payroll': payroll})

@staff_member_required
def hr_payroll_list(request):
    payrolls = Payroll.objects.select_related('employee_user').all()
    return render (request, 'tasks/hr_payroll_list.html', {'payrolls': payrolls})
