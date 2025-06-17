from django.shortcuts import render

# Create your views here.

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request,'login.html')

def home(request):
    return render(request,'home.html')
