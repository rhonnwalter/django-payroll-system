from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='redirect_dashboard'),
    path('dashboard/employee', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/hr', views.hr_dashboard, name='hr_dashboard'),

    path('my-payroll/', views.my_payroll, name='my_payroll'),
    path('payrolls/<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('payroll-history/<int:employee_id>/', views.payroll_history, name='payroll_history'),
    path('hr/employees/', views.employee_list, name='employee_list'),
    path('hr/employee/<int:employee_id>/payrolls/',views.employee_payrolls, name='employee_payrolls'),
    
    path('hr/payrolls/', views.hr_payroll_list, name='hr_payroll_list'),
    path('hr/create-payroll/', views.create_payroll, name='create_payroll'),
    path('hr/create-employee/', views.create_employee, name='create_employee'),
    path('hr/mark-paid/<int:pk>', views.mark_paid, name='mark_paid'),
    
   


]