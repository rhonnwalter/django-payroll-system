from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='redirect_dashboard'),
    path('dashboard/employee', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/hr', views.hr_dashboard, name='hr_dashboard'),


    path('payrolls/', views.my_payroll, name='my_payroll'),
    path('payrolls/<int:pk>/', views.payroll_detail, name='payroll_detail'),
    
    path('hrpayrolls/', views.hr_payroll_list, name='hr_payroll_list'),

    path('dashboard/employees/', views.employee_list, name='employee_list'),


]