from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Car

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
    return render(request,'home.html')

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

