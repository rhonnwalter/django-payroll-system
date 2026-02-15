from django.contrib import admin
from .models import Employee, Payroll

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'position',
        'hourly_rate',
        'is_active',
        'date_hired',
        )

class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'payroll_period', 
        'total_pay',
        'created_by',
        'created_at',
        'updated_at'
        
        )
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    #Shows Employee, Payroll Period, and Created At columns in the list view.

    readonly_fields = ('created_at','created_by')
    #Prevents accidentally changing the timestamp.

    list_filter = ('payroll_period', 'created_at', )
    #Lets you filter payrolls by period or creation date quickly.
    search_fields = ('employee__first_name', 'employee__last_name', 'payroll_period')
    #Lets you search payrolls by employee name or payroll period.

    ordering = ('payroll_period', 'employee')
    #Shows the most recent payrolls at the top by default.

    


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Payroll, PayrollAdmin)