from django.urls import path
from .import views

urlpatterns = [
    path('admin-portal-72e9b', views.admin_dashboard, name='admin_dashboard'),
]
