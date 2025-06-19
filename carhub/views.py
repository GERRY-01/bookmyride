import base64
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Car
import requests
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime
from requests.auth import HTTPBasicAuth

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
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exists")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request,"Email already exists")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                messages.success(request,"Account created successfully")
                return redirect("home")
        else:
            messages.error(request,"Passwords do not match")
            return redirect("register") 
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            auth_login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Invalid credentials")
    return render(request,'login.html')

def home(request):    
    cars = Car.objects.all()
    return render(request,'home.html',{'cars':cars})

def admin_page(request): 
    if request.method == 'POST':
        image = request.FILES.get("image")
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        cars = Car(image=image,name=name,description=description,price_per_day=price)
        cars.save()
        
    Cars = Car.objects.all()        
    return render(request,'adminpage.html',{'Cars':Cars})

def delete_car(request,car_id):
    car = Car.objects.get(id=car_id)
    car.delete()
    return redirect("admin_page")

def update_car(request,car_id):
    car = Car.objects.get(id=car_id)
    if request.method == 'POST':
        image = request.FILES.get("image")
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        
        if image:
           car.image = image
        car.name = name
        car.description = description
        car.price_per_day = price
        car.save()
        return redirect("admin_page")
    return render(request,'update_car.html',{'car':car})

def logout_user(request):
    is_admin = request.user.is_staff
    logout(request)
    if is_admin:
        return redirect("admin_dashboard")
    return redirect("home")

# Integrating my app with mpesa API

def get_access_token(request):
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return r.json()['access_token']

def lipa_na_mpesa_online(request):
    if request.method == 'POST':
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(data_to_encode.encode()).decode()
        
        access_token = get_access_token(request)
        api_url = settings.MPESA_BASE_URL
        headers = {"Authorization": "Bearer %s" % access_token}
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": "https://mydomain.com/payload",
            "AccountReference": "Car Booking",
            "TransactionDesc": "Payment of Car Booking"
        }
        
        res = requests.post(api_url, json=payload, headers=headers)
        return JsonResponse(res.json())
    return render(request,'home.html')