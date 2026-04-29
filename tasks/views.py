from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,  render, get_object_or_404
from .models import Employee, Payroll, Attendance
from django.utils import timezone
from .forms import EmployeeForm, AttendanceForm, GeneratePayrollForm
from services.hr_dashboard import hr_dashboard_stats
from services.employee_services import filter_employees, create_employee_service
from services.attendance_service import filter_attendances, get_attendance_detail, create_attendance_service
from services.payroll_services import filter_payrolls, mark_payroll_paid, get_payroll_detail, get_payroll_history,  get_current_month_payrolls
from services.payroll_generate import generate_payroll as generate_payroll_service
from services.query_services import paginate_queryset
from services.permission_services import hr_required

@login_required
@hr_required
def employee_list(request):
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
@hr_required
def attendance_list(request):
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
def attendance_detail(request, pk):
    attendance = get_attendance_detail(request.user, pk)
    return render (request, 'dashboard/attendance_detail.html', {'attendance':attendance} )

@login_required
def my_attendance(request):
    attendances = Attendance.objects.select_related('employee__user').filter(employee__user = request.user)
    return render (request, 'dashboard/my_attendance.html', {'attendances':attendances})

@login_required
@hr_required
def employee_payrolls(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    payrolls = Payroll.objects.select_related('employee__user').filter(employee=employee).order_by('-payroll_period_start')

    return render(request, 'dashboard/employee_payrolls.html', {
        'employee' : employee,
        'payrolls': payrolls
    })

@login_required
def my_payroll(request):
    payroll= Payroll.objects.select_related('employee__user').filter(employee__user=request.user).order_by('-payroll_period_start').first()
    
    return render (request, 'dashboard/my_payroll.html', {'payroll':payroll})

@login_required
def payroll_detail(request, pk):
    payroll = get_payroll_detail(request.user, pk)
    return render (request, 'dashboard/payroll_detail.html', {'payroll': payroll})

@login_required
@hr_required
def mark_paid(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    mark_payroll_paid(payroll, user=request.user)
    return redirect ('hr_payroll_list')

@login_required
def payroll_history(request, employee_id=None):
    payrolls = get_payroll_history(request.user, employee_id)

    page_obj = paginate_queryset (request, payrolls)
    context = {
        'page_obj' : page_obj
    }
    return render (request, 'dashboard/payroll_history.html', context)


@login_required
@hr_required
def hr_payroll_list(request):
    search = (request.GET.get('search') or '').strip()
        
    payrolls = get_current_month_payrolls()
    payrolls = filter_payrolls(payrolls, search)
    payrolls = payrolls.order_by('-payroll_period_start')

    page_obj = paginate_queryset(request, payrolls)

    context = {
                'page_obj' : page_obj,
                'search_query' : search
    }
   
    return render (request, 'dashboard/hr_payroll_list.html', context)

@login_required
@hr_required
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
@hr_required
def create_attendance(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
           create_attendance_service(form)
           return redirect('attendance_list')
    else: form = AttendanceForm()

    return render(request, 'dashboard/create_attendance.html', {'form': form})

 
@login_required
@hr_required
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

    if user.is_staff:
        return redirect('hr_dashboard')
    
    else:  
        return redirect('employee_dashboard')
   

@login_required
@hr_required
def hr_dashboard(request):
    stats = hr_dashboard_stats(request)
    return render(request, 'dashboard/hr_dashboard.html', stats)

@login_required
def employee_dashboard(request):
    payrolls = Payroll.objects.select_related('employee__user').filter(employee__user=request.user).order_by('-created_at')
    latest_payroll = payrolls.first()
    total_payrolls = payrolls.count()

    context = {
        'latest_payroll' : latest_payroll,
        'total_payrolls' : total_payrolls,

    }
    return render (request, 'dashboard/employee_dashboard.html', context)



