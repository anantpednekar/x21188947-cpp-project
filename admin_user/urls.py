from django.urls import path
from . import views

app_name = 'admin_user'

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('create_clinic/', views.create_clinic, name='create_clinic'),    
    path('clinic_delete/<int:pk>/', views.clinic_delete, name='clinic_delete'),
]