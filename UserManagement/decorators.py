from django.http import HttpResponse
from django.shortcuts import redirect

def admin_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_admin and request.user.is_active and request.user.company.active:            
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func

def interviewer_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_interviewer and request.user.is_active:
            return view_func(request, *args, **kwargs)
        else:
             return HttpResponse('You are not authorized to access this content.')
    return wrapper_func


def admin_super_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:            
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func






