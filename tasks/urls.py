from django.urls import path
from . import views


urlpatterns = [
    path('payrolls/', views.payroll_list, name='payroll_list'),
    path('payrolls/<int:pk>/', views.payroll_detail, name='payroll_detail'),


]