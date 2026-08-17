from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='redirect_dashboard'),
    path('dashboard/employee', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/hr', views.hr_dashboard, name='hr_dashboard'),

    path('my-attendace/', views.my_attendance, name='my_attendace'),
    path('attendance-detail/<int:pk>', views.attendance_detail, name='attendace_detail'),
   

    path('my-payroll/', views.my_payroll, name='my_payroll'),
    path('payroll-detail/<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('payroll-history/<int:employee_id>/', views.payroll_history, name='payroll_history'),

    path('hr/attendace-list/', views.attendance_list, name='attendance_list'),
    path('hr/record-attendance/', views.record_attendance, name='record_attendance'),
    path('hr/employees-list/', views.employee_list, name='employee_list'),
    path('hr/employees/<int:employee_id>/payrolls/',views.employee_payrolls, name='employee_payrolls'),
    path('hr/payrolls-list/', views.hr_payroll_list, name='hr_payroll_list'),

    path('hr/edit-employee/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('hr/delete-employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('hr/create-employee/', views.create_employee, name='create_employee'),
    path('hr/get-positions/', views.get_positions, name='get_position'),
    path('hr/generate-payrolls/', views.generate_payroll, name='generate_payroll'),
    path('hr/mark-paid/<int:pk>', views.mark_paid, name='mark_paid'),
    
   


]