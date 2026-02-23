from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Employee, Payroll
from django.utils import timezone



# Create your views here.
def employee_list(request):
    employees = Employee.objects.all()
    return render (request, 'dashboard/employee_list.html', {'employees':employees})

def my_payroll(request):
    payroll= Payroll.objects.filter(employee__user=request.user).first()
    return render (request, 'dashboard/my_payroll.html', {'payroll':payroll})

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
    return render (request, 'dashboard/payroll_detail.html', {'payroll': payroll})
@login_required
def payroll_history(request, employee_id=None):
    if request.user.is_superuser:
        payrolls = Payroll.objects.filter(employee_id=employee_id). order_by('-payroll_period')
    else:
        payrolls = Payroll.objects.filter(
            employee__user=request.user
        ).order_by('payroll_period')
    context = {
        'payrolls' : payrolls
    }
    return render (request, 'dashboard/payroll_history.html', context)

def hr_required(view_func):
    def wrapper(request, *args, **kwargs): # *args collects extra positional arguments. **kwargs collects extra keyword arguments.
        if not request.user.is_superuser: 
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return wrapper

@staff_member_required
@hr_required

def hr_payroll_list(request):
    search = request.GET.get('search', '')
    
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    payrolls = Payroll.objects.select_related('employee__user').filter(
        payroll_period__month=current_month,
        payroll_period__year=current_year
    )

    if search: 
        payrolls = payrolls.filter (
            Q(employee__user__username__icontains=search) |
            Q(employee__position__icontains=search) |
            Q(payroll_period__icontains=search)
        )
    
    payrolls = payrolls.order_by('-payroll_period')

    paginator = Paginator(payrolls, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) #this displays the per page payrolls with the applied paginator of 10 per pages

    context = {
        'page_obj' : page_obj,
        'search_query' : search
    }
    return render (request, 'dashboard/hr_payroll_list.html', context)


@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser:
        return redirect('hr_dashboard')
    
    elif user.is_staff:
        return redirect('hr_dashboard')
    
    else:  
        return redirect('employee_dashboard')
    
from django.db.models import Sum
def hr_dashboard(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    payrolls = Payroll.objects.annotate(total_pay_expr=Payroll.total_pay_expression())
    total_employees = Employee.objects.count()
    total_payrolls = payrolls.count()
    total_salary = payrolls.aggregate(Sum('total_pay_expr'))['total_pay_expr__sum'] or 0 #['total_pay_expr__sum' grab the actual number from the dictionary.
    context = {
        'payrolls' : payrolls,
        'total_employees' : total_employees,
        'total_payrolls' : total_payrolls,
        'total_salary' : total_salary

    }
    return render(request, 'dashboard/hr_dashboard.html', context)

@login_required
def employee_dashboard(request):
    payrolls = Payroll.objects.filter(employee__user=request.user).order_by('-created_at')
    latest_payroll = payrolls.first()
    total_payrolls = payrolls.count()

    context = {
        'latest_payroll' : latest_payroll,
        'total_payrolls' : total_payrolls,

    }
    return render (request, 'dashboard/employee_dashboard.html', context)



