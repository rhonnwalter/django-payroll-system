from django.contrib import admin
from .models import Employee, Payroll, Attendance, Department, Position

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id',
        'last_name',
        'first_name',
        'user',
        'position',
        'hourly_rate',
        'department',
        'employee_type',
        'is_active',
        'date_hired',
        )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
    )

class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'department',
    )

class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'date',
        'regular_hours',
        'overtime_hours',
        'created_by'
    )
    list_filter = ('date', 'employee')
    search_fields = ('employee__user__username',)
    ordering = ('-date',)

class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'payroll_period_start', 
        'status',
        'gross_pay',
        'net_pay',
        'created_at',
        'updated_at'
        
        )
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
  
    readonly_fields = ('created_at','created_by')
    #Prevents accidentally changing the timestamp.

    list_filter = ('status','payroll_period_start', 'created_at')
    #Lets you filter payrolls by period or creation date quickly.
    search_fields = ('employee__first_name', 'employee__last_name', 'payroll_period_start')
    #Lets you search payrolls by employee name or payroll period.

    ordering = ('payroll_period_start', 'employee')
    #Shows the most recent payrolls at the top by default.

    

admin.site.register(Position, PositionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(Department, DepartmentAdmin)

