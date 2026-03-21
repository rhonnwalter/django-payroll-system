from decimal import Decimal, ROUND_HALF_UP
from django.db.models import F,Case,When,ExpressionWrapper, DecimalField, Value

def compute_total_pay(employee, total_regular_hours, total_overtime_hours):
        
        if employee.pay_type == "hourly":
            total = (
                total_regular_hours * employee.hourly_rate +
                total_overtime_hours * employee.overtime_multiplier
            )
        elif employee.pay_type == "salary":
            total = employee.salary_per_period
        else:
            total = Decimal('0.00')

        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) #sets the precision as 2. decimal places.

def total_pay_expression():
        return ExpressionWrapper(
            Case(
                When(employee__pay_type="hourly",
                     then=(F('total_regular_hours')  * F('employee__hourly_rate') +
                     F('total_overtime_hours') * F('employee__overtime_multiplier')
                    )
                ),
                When(employee__pay_type="salary",
                    then=(F('employee__salary_per_period') 
                    ) 
                ),
                default=Value(Decimal('0.00'))
            
            ), 
            output_field=DecimalField(max_digits=10, decimal_places=2)  
         
         )

def compute_sss_employee_share(gross_pay):
    sss_table = [
            (4250, 180), (5000, 225), (10000, 450),
            (20000, 900), (30000, 1350)
        ]

    for salary, contribution in sss_table:
      if gross_pay <= salary:
        return Decimal(contribution)
      
    return Decimal("1350")

def compute_philhealth(gross_pay):
    employee = gross_pay * Decimal("0.015")
    employer = gross_pay * Decimal("0.015") 
    return {"Employee" : employee, "Employer" : employer}

def compute_pagibig(gross_pay):
     employee = min(gross_pay * Decimal("0.02"), Decimal("100"))
     employer = gross_pay * Decimal("0.02")
     return {"Employee":employee, "Employer":employer}

def compute_total_deductions(gross_pay):
     sss = compute_sss_employee_share(gross_pay)
     philhealth = compute_philhealth(gross_pay)["Employee"]  
     pagibig = compute_pagibig(gross_pay)["Employee"]

     tax = compute_income_tax(gross_pay)
     total_deductions = sss + philhealth + pagibig + tax

     return {
          "sss":sss,
          "philhealth":philhealth,
          "pagibig":pagibig,
          "tax":tax,
          "total":total_deductions
     }

def compute_income_tax(gross_pay):
         
      if gross_pay <= 20833:
            return Decimal("0.00")
      elif gross_pay <= 33332:
            return (gross_pay - Decimal("20833")) * Decimal("0.15")
      elif gross_pay <= 66666:
            return (gross_pay - Decimal("33332")) * Decimal("0.20")
      elif gross_pay <= 166666:
            return (gross_pay - Decimal("66666")) * Decimal("0.25")
      elif gross_pay <= 666667:
            return (gross_pay - Decimal("166666")) * Decimal("0.30")
      else:
        return Decimal("183541.67") + (gross_pay - Decimal("666667")) * Decimal("0.35")
      
def compute_netpay(gross_pay):
     deductions = compute_total_deductions
     net = gross_pay - deductions["total"]

     return net.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), deductions