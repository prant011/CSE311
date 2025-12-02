"""
Custom decorators for the library application.
"""
from django.shortcuts import redirect
from django.contrib import messages

def login_required_message(view_func):
    """
    Decorator that checks if the user is logged in.
    If not, redirects to the login page with a message.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    """
    Decorator that checks if the user is an admin.
    If not, redirects to the home page with a message.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.warning(request, 'You do not have permission to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
