import functools
from django.shortcuts import redirect, get_object_or_404, render 
from django.contrib import messages
from .models import AccountModel

def authentication_not_required(view_func, redirect_url="home"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request,*args, **kwargs)
        print("You need to be logged out")
        return redirect(redirect_url)
    return wrapper

def authentication_required(view_func, redirect_url="home"):
    @functools.wraps(view_func)
    def innner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request,*args, **kwargs)
        print("You need to be logged out")
        return redirect(redirect_url)
    return innner

def verification_required(view_func, verification_url="accounts:activate_email"):
    """
        this decorator restricts users who have not been verified
        from accessing the view function passed as it argument and
        redirect the user to page where their account can be activated
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_active:
            return view_func(request, *args, **kwargs)
        messages.info(request, "Email verification required")
        print("You need to be logged out")
        return redirect(verification_url)  
    return wrapper

def author_req(view_func, redirect_url="home"):#maqolasi borligiga tekshirish
    @functools.wraps(view_func)
    def wrapper(request, username, *args, **kwargs):
        person = get_object_or_404(AccountModel, username=username)
        if person.role=='A':
            return view_func(request, username, *args, **kwargs)
        return render(request=request, template_name='not_found.html')
    return wrapper

def author_create(view_func):#maqolasi borligiga tekshirish
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        person = get_object_or_404(AccountModel, username=request.user.username)
        if person.role=='A':
            return view_func(request, *args, **kwargs)
        return render(request=request, template_name='not_found.html')
    return wrapper

