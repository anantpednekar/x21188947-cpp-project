from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('delete_appointment/<int:pk>/', views.delete_appointment_view, name='delete_appointment'),
    path('schedule_appointment/', views.schedule_appointment_view, name='schedule_appointment'),
    path('update_user/', views.update_user_view, name='update_user_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_user_view, name='register_user_view'),
]
