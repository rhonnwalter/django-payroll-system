from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# MODELS
def validate_half_hour(value): #validator for decimal .50 in hours_worked and overtime_hours
    if (value * 100) % 50 != 0: 
        raise ValidationError('Hours must be in increments of 0.50') 
    
class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.code} - {self.name}"

class Position(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="positions")
    def __str__(self):
        return f"{self.title} - ({self.department.name})"

class Employee(models.Model):
    PAY_TYPE_CHOICES = [
        ('hourly', 'Hourly'),
        ('salary', 'Salary'),
    ]
    EMPLOYEE_TYPE_CHOICES = [
        ('FULLTIME', 'Full-time'),
        ('PARTTIME',  'Part-time'),
        ('INTERN',  'Intern'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True, editable = False)

    first_name = models.CharField(max_length=150, null=False, blank=False)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    profile_picture = models.ImageField(upload_to='employee_pics/', null=True, blank=False)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    employee_type = models.CharField(max_length=10, choices=EMPLOYEE_TYPE_CHOICES, default='FULLTIME')
    pay_type = models.CharField(max_length=10, choices=PAY_TYPE_CHOICES, default='hourly')

    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    salary_per_period = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overtime_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.5)
    

    is_active = models.BooleanField(default = True)
    date_hired = models.DateTimeField(auto_now_add=True)

    def full_name(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_emp = Employee.objects.order_by('-id').first()
            if last_emp and last_emp.employee_id:
                last_num = int(last_emp.employee_id.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.employee_id = f'EMP-{new_num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.employee_id} - {self.user.username}'

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    
    regular_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[validate_half_hour],
        default=0 
        )
    overtime_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_half_hour],
        default=0
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False
        
        )
    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

def __str__(self):
    return f"{self.employee.username} - {self.date}"

    
class Payroll(models.Model):
    employee = models.ForeignKey(Employee ,on_delete=models.CASCADE)

    payroll_period_start = models.DateField(null=True, blank=True)
    payroll_period_end = models.DateField(null=True, blank=True)

    total_regular_hours = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[validate_half_hour],
        default=0
    )
    
    total_overtime_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[validate_half_hour],
        default=0
        
    )
    
    sss = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    philhealth = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagibig = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)



    gross_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    status_choices = (
        ('pending', 'Pending'), #first element is the actual value passed to db, second element is what is readable to admin
        ('paid', 'Paid'),
    )

    status = models.CharField(max_length=10, choices=status_choices, default='pending' )

    class Meta:
        unique_together = ('employee', 'payroll_period_start', 'payroll_period_end')
        ordering = ['-payroll_period_start']
    


    def __str__(self):
        return f"Payroll - {self.employee.user.username}"
  


