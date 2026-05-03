from django.db.models import Q
from tasks.models import Payroll
from django.core.paginator import Paginator

def filter_payrolls(queryset, search=None):
    if search: 
        search_condition = (
            Q(employee__user__username__icontains=search) |
            Q(employee__position__icontains=search)  |
            Q(employee__department__icontains=search)  |
            Q(employee__pay_type__icontains=search)  
        )

        queryset = Payroll.filter(search_condition)

    return queryset

def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')

    return paginator.get_page(page_number)

