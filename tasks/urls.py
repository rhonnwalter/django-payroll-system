from django.urls import path
from . import views


urlpatterns = [
    path('payrolls/', views.my_payroll, name='my_payroll'),
    path('payrolls/<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('hrpayrolls/', views.hr_payroll_list, name='hr_payroll_list')


]