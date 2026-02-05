from django.urls import path
from . import views


urlpatterns = [
    path('payrolls/', views.payroll_list, name='payroll_list'),
    path('payrolls/<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('hrpayrolls/', views.hr_payroll_list, name='hr_payroll_list')


]