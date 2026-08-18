from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, request
from django.shortcuts import redirect,  render, get_object_or_404
from .models import Employee, Payroll, Department
from .forms import EmployeeForm, AttendanceForm, GeneratePayrollForm, UserForm
from .services.hr_dashboard import hr_dashboard_stats
from .services.employee_dashboard import employee_dashboard
from .services.employee_services import filter_employees, filter_positions_by_department,get_base_employee, department_list
from .services.attendance_service import filter_attendances, get_attendance_detail, create_attendance_service, get_base_attendance, get_my_attendance
from .services.payroll_services import filter_payrolls, mark_payroll_paid, get_payroll_detail, get_payroll_history,  get_base_payroll, get_employee_payroll
from .services.payroll_generate import generate_payroll as generate_payroll_service
from .services.query_services import paginate_queryset
from .services.permission_services import hr_required
import datetime

@login_required
@hr_required
def employee_list(request):
    search = (request.GET.get('search') or '').strip()
   
    employees = get_base_employee()
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
def get_positions(request):
    dept_id = request.GET.get('department_id')
    positions = filter_positions_by_department(dept_id)
    return JsonResponse(list(positions), safe=False)

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    user = employee.user
    
    if request.method == "POST":
        emp_form = EmployeeForm(request.POST, request.FILES, instance=employee)
        user_form = UserForm(request.POST, instance=user)


        if emp_form.is_valid() and user_form.is_valid() :
            print('Cleaned data:', user_form.cleaned_data)
            print('Cleaned data:', emp_form.cleaned_data)
            with transaction.atomic():
                user_form.save()
                emp_form.save()
                messages.success (request, 'Employee and User details updated successfully')
                return redirect ('employee_list')
        else:
             messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=user)
        emp_form = EmployeeForm(instance=employee)
    return render (request, 'dashboard/edit_employee.html', {'user_form':user_form,'emp_form':emp_form, 'employee':employee})

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect ('employee_list')
    return render (request, 'dashboard/confirm_delete.html' )
    
@login_required
@hr_required
def attendance_list(request):
    search = (request.GET.get('search') or '').strip()
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    attendances = get_base_attendance()
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
    attendances = get_my_attendance(request.user)
    return render (request, 'dashboard/my_attendance.html', {'attendances':attendances})

@login_required
@hr_required
def employee_payrolls(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    payrolls = get_employee_payroll(employee)

    return render(request, 'dashboard/employee_payrolls.html', {
        'employee' : employee,
        'payrolls': payrolls
    })

@login_required
def my_payroll(request):
    payroll= my_payroll(request.user)
    
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

    department = (request.GET.get('department'))
    month = int(request.GET.get('month', datetime.date.today().month))
    year = int(request.GET.get('year', datetime.date.today().year))

    months = range(1, 13)
    current_year=datetime.datetime.today().year
    years = range(2024, current_year + 1)

    queryset = get_base_payroll()
    payrolls = filter_payrolls(queryset, department, search, month, year)
    payrolls = payrolls.order_by('-payroll_period_start')

    page_obj = paginate_queryset(request, payrolls)

    context = {
                'search_query' : search,
                'department' : department, 
                'departments' : Department.objects.all(),
                'month' : month,
                'year' : year,
                'months': months,
                'years': years,
                'page_obj' : page_obj,
    }
   
    return render (request, 'dashboard/hr_payroll_list.html', context)

@login_required
@hr_required
def create_employee(request):
    if request.method == "POST":
            user_form = UserForm(request.POST)
            emp_form = EmployeeForm(request.POST, request.FILES)
            if emp_form.is_valid() and user_form.is_valid():
                try:
                    user = user_form.save()
                    employee = emp_form.save(commit=False)
                    employee.user = user
                    employee.save()
                    messages.success(request, "Employee Created Successfully")
                    return redirect ('employee_list')
                
                except ValueError as e:
                    messages.error(request, str(e))

    else:
        emp_form = EmployeeForm()
        user_form = UserForm()

    departments = department_list() 

    return render(request, 'dashboard/create_employee.html', {
        'emp_form': emp_form,
        'user_form': user_form,
        'departments': departments
    })  
       
@login_required
@hr_required
def record_attendance(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
           create_attendance_service(form, request.user)
           return redirect('attendance_list')
    else: form = AttendanceForm()

    return render(request, 'dashboard/record_attendance.html', {'form': form})

 
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
    payrolls = employee_dashboard(request.user)
    latest_payroll = payrolls.first()
    total_payrolls = payrolls.count()

    context = {
        'latest_payroll' : latest_payroll,
        'total_payrolls' : total_payrolls,

    }
    return render (request, 'dashboard/employee_dashboard.html', context)



