from django.urls import path
from .import views

urlpatterns = [
    path('admin-login-72e9b', views.admin_login, name='admin_login'),
    path('admin-register',views.admin_register,name='admin_register'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('',views.home,name='home'),
    path('admin_page',views.admin_page,name="admin_page"),
    path('admin_page/delete_car/<int:car_id>', views.delete_car, name='delete_car'),
    path('admin_page/update_car/<int:car_id>', views.update_car, name='update_car'),
    path('logout_user',views.logout_user,name='logout'),
    path('lipa_na_mpesa_online',views.lipa_na_mpesa_online,name='lipa_na_mpesa_online'),
]
