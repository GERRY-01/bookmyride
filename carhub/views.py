from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def admin_dashboard(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None and user.is_staff:
            auth_login(request,user)
            return redirect("admin_page")
        else:
            messages.error(request,"Invalid credentials")
        
    return render(request, 'admin_dashboard.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request,'login.html')

def home(request):
    return render(request,'home.html')

def admin_page(request):
    return render(request,'adminpage.html')
