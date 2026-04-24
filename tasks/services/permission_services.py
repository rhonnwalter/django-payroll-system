from django.http import HttpResponseForbidden
def hr_required(view_func):
    def wrapper(request, *args, **kwargs): # *args collects extra positional arguments. **kwargs collects extra keyword arguments.
        if not (request.user.is_superuser or request.user.is_staff): 
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return wrapper

def is_hr(user):
    return user.is_staff or user.is_superuser

def is_owner(user, obj):
    return obj.employee.user == user