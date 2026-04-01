from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Employee, Payroll, Attendance
from django.utils import timezone
from .forms import EmployeeForm, AttendanceForm, GeneratePayrollForm
from datetime import datetime
from decimal import Decimal

from .services import compute_total_pay, compute_total_deductions, compute_netpay

def hr_required(view_func):
    def wrapper(request, *args, **kwargs): # *args collects extra positional arguments. **kwargs collects extra keyword arguments.
        if not request.user.is_superuser: 
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
# Create your views here.
def employee_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed here.")
    
    search = (request.GET.get('search') or '').strip()

    employees = Employee.objects.select_related('user').filter(is_active=True)

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
        employees = employees.filter(search_condition)

    employees = employees.order_by('-is_active', 'user__last_name', 'user__last_name')
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'search_query' : search,
        'page_obj': page_obj
    
    }

    return render (request, 'dashboard/employee_list.html', {context})

@login_required
def attendance_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed here.")
    
    attendances = Attendance.objects.select_related('employee__user').filter(employee__is_active=True)

    search = (request.GET.get('search') or '').strip()
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_from:
        try: 
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        except ValueError: 
            date_from = None

    if date_to:
        try: 
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError:
            date_to = None

    if date_from:
        attendances = attendances.filter(date__gte=date_from)

    if date_to:
        attendances = attendances.filter(date__lte=date_to)
            
    if search:
        search_condition = (
            Q(employee__user__username__icontains=search) |
            Q(employee__user__first_name__icontains=search) |
            Q(employee__user__last_name__icontains=search) |
            Q(employee__department__icontains=search) 

        )
        attendances = attendances.filter(search_condition)

    attendances = attendances.order_by('-date', 'employee__user__last_name', 'employee__user__first_name')
    paginator = Paginator(attendances, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'search_query' : search,
        'page_obj': page_obj,
        'date_from' : date_from,
        'date_to' : date_to
    
    }

    return render (request, 'dashboard/attendance_list.html', context)

@login_required
def attendace_detail(request,pk):
    if request.user.is_staff or request.user.is_superuser:
        attendance = get_object_or_404(Attendance, pk=pk)
    else: 
        attendance = get_object_or_404(
            Attendance, 
            pk=pk,
            employee__user = request.user
        )
    return render (request, 'dashboard/attendace_detail.html', {'attendances':attendance} )
@login_required
def my_attendance(request):
    Attendance.objects.filter(employee__user = request.user).first()
    return render (request, 'dashboard/my_attendance.html', {'attendances':Attendance})

@login_required
def employee_payrolls(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if not request.user.is_superuser and request.user !=employee.user:
            return render(request, 'dashboard/not_authorized.html')
    
    payrolls = Payroll.objects.filter(employee=employee).order_by('-payroll_period_start')

    return render(request, 'dashboard/employee_payrolls.html', {
        'employee' : employee,
        'payrolls': payrolls
    })
@login_required
def my_payroll(request):
    payroll= Payroll.objects.filter(employee__user=request.user).first()
    return render (request, 'dashboard/my_payroll.html', {'payroll':payroll})
@login_required
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

@staff_member_required
def mark_paid(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    payroll.status = 'paid'
    payroll.save()
    return redirect ('hr_payroll_list')

@login_required
def payroll_history(request, employee_id=None):
    if request.user.is_superuser:
        payrolls = Payroll.objects.filter(employee_id=employee_id). order_by('-payroll_period_start')
    else:
        payrolls = Payroll.objects.filter(
            employee__user=request.user
        ).order_by('payroll_period_start')

    paginator = Paginator(payrolls, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj' : page_obj
    }
    return render (request, 'dashboard/payroll_history.html', context)




@login_required
def hr_payroll_list(request):

    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed here.") 
    
    search = (request.GET.get('search') or '').strip()
        
    now = timezone.now()
    current_month = now.month
    current_year = now.year
        
    payrolls = Payroll.objects.select_related('employee__user').filter(
            employee__is_active=True,
            payroll_period_start__month=current_month,
            payroll_period_start__year=current_year,
 
        )


    if search: 
        search_condition = (
            Q(employee__user__username__icontains=search) |
            Q(employee__position__icontains=search)  |
            Q(employee__department__icontains=search)  |
            Q(employee__pay_type__icontains=search)  
        )

        payrolls = payrolls.filter(search_condition)
        
    payrolls = payrolls.order_by('-payroll_period_start')

    paginator = Paginator(payrolls, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) #this displays the per page payrolls with the applied paginator of 10 per pages

    context = {
                'page_obj' : page_obj,
                'search_query' : search
    }
  
       
    return render (request, 'dashboard/hr_payroll_list.html', context)

from django.contrib.auth.models import User
login_required
@user_passes_test(hr_required)
def create_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=username,
                password=password
            )
            employee = form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect ('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'dashboard/create_employee.html', {'form': form} )  
       
@login_required
@user_passes_test(hr_required)
def create_attendance(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('dashboard/attendance_list.html')
    else: form = AttendanceForm

    return render(request, 'dashboard/create_attendance.html', {'form': form})


@login_required
@user_passes_test(hr_required)
def generate_payroll(request):
    if request.method == "POST":
        form = GeneratePayrollForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            employees = Employee.objects.filter(is_active=True)

            for employee in employees:

                if Payroll.objects.filter(
                        employee=employee,
                        payroll_period_start=start_date,
                        payroll_period_end=end_date
                    ).exists():
                        continue
                
                if employee.pay_type == "hourly":
                    attendance_records = Attendance.objects.filter(
                    employee=employee,
                    date__range=[start_date, end_date]
                    )
                    total_regular = Decimal(sum(a.regular_hours for a in attendance_records))
                    total_overtime = Decimal(sum(a.overtime_hours for a in attendance_records))

                    gross_pay = compute_total_pay(employee, total_regular, total_overtime)

                elif employee.pay_type == "salary":
                    total_regular = Decimal("0.00")
                    total_overtime = Decimal("0.00")
                    gross_pay = employee.salary_per_period
                
                else:
                    continue
                
                net_pay, deductions = compute_netpay(gross_pay)

                payroll = Payroll(
                    employee=employee,
                    payroll_period_start=start_date,
                    payroll_period_end=end_date,
                    total_regular_hours=total_regular,
                    total_overtime_hours=total_overtime,
                    gross_pay=gross_pay,
                    net_pay=net_pay
                )
                payroll.sss = deductions["sss"]
                payroll.philhealth = deductions["philhealth"]
                payroll.pagibig = deductions["pagibig"]
                payroll.tax = deductions['tax']

                payroll.save()

        
        return redirect("hr_dashboard")
    else: 
        form = GeneratePayrollForm()
    
    return render (request, "dashboard/generate_payroll.html", {"form": form})
    

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
@login_required
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



