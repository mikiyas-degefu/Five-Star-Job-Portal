from django.http import HttpResponse
from django.shortcuts import redirect

def admin_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_admin:            
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func

def interviewer_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_interviewer:
            return view_func(request, *args, **kwargs)
        else:
             return HttpResponse('You are not authorized to access this content.')
    return wrapper_func

