from django.urls import path
from .import views

urlpatterns = [
    path('admin-portal-72e9b', views.admin_dashboard, name='admin_dashboard'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('home',views.home,name='home'),
    path('admin_page',views.admin_page,name="admin_page"),
    path('admin_page/delete_car/<int:car_id>', views.delete_car, name='delete_car'),
    path('admin_page/update_car/<int:car_id>', views.update_car, name='update_car'),
    path('logout_user',views.logout_user,name='logout'),
]
