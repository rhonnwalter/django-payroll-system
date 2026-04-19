from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum
from .models import Employee, Payroll, Attendance
from django.utils import timezone
from .forms import EmployeeForm, AttendanceForm, GeneratePayrollForm
from services.employee_services import filter_employees, create_employee_service
from services.attendance_service import filter_attendances
from services.payroll_services import filter_payrolls
from services.payroll_generate import generate_payroll as generate_payroll_service
from services.query_services import paginate_queryset


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

   
    employees = filter_employees(employees, search=search)

    employees = employees.order_by('-is_active', 'user__last_name', 'user__first_name')
    page_obj = paginate_queryset(request, employees)

    context = {
        'search_query' : search,
        'page_obj': page_obj
    
    }

    return render (request, 'dashboard/employee_list.html', context)

@login_required
def attendance_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed here.")
    
    search = (request.GET.get('search') or '').strip()
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    attendances = Attendance.objects.select_related('employee__user').filter(employee__is_active=True)

    attendances = filter_attendances(attendances, search=search, date_from=date_from, date_to=date_to)

    attendances = attendances.order_by('-date', 'employee__user__last_name', 'employee__user__first_name')
    page_obj = paginate_queryset(request, attendances)

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
    attendances = Attendance.objects.filter(employee__user = request.user).first()
    return render (request, 'dashboard/my_attendance.html', {'attendances':attendances})

@login_required
def employee_payrolls(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if not (request.user.is_superuser or request.user.is_staff or request.user==employee.user):
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
        if employee_id:
             payrolls = Payroll.objects.filter(employee_id=employee_id).order_by('-payroll_period_start')
        else:
            payrolls = Payroll.objects.all().order_by('-payroll_period_start')
    else:
        payrolls = Payroll.objects.filter(
            employee__user=request.user
        ).order_by('payroll_period_start')

    page_obj = paginate_queryset (request, payrolls)
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

    payrolls = filter_payrolls(payrolls, search)
        
    payrolls = payrolls.order_by('-payroll_period_start')

    page_obj = paginate_queryset(request, payrolls)

    context = {
                'page_obj' : page_obj,
                'search_query' : search
    }
   
    return render (request, 'dashboard/hr_payroll_list.html', context)

@login_required
@user_passes_test(hr_required)
def create_employee(request):
    if request.method == "POST":
            form = EmployeeForm(request.POST)
            if form.is_valid():
                create_employee_service(form)
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
           return redirect('attendance_list')
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

            generate_payroll_service(start_date, end_date)
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



