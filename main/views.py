from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from myLibrary.mainLogger import myCustomLogger
import datetime
from admin_user.models import Clinic
from main.models import Appointment, UserProfile
from .forms import AppointmentForm, RegistrationForm, UpdateUserForm

logger = myCustomLogger('main.views', 'DEBUG')

@login_required  
def delete_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    logger.info(f"Appointment with pk={pk} deleted by {request.user} at {datetime.datetime.now()}")
    return redirect('main:index')

@login_required
def schedule_appointment_view(request):
    clinics = Clinic.objects.all()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            #messages.success(request, 'Appointment scheduled successfully!')
            logger.debug(f"Appointment scheduled successfully by {request.user} at {datetime.datetime.now()} ") 
            return redirect('main:index')
    else:
        form = AppointmentForm()
    return render(request, 'main/schedule_appointment.html', {'form': form, 'clinics': clinics})

@login_required
def update_user_view(request):
    user = request.user
    user_profile = user.userprofile  # get the UserProfile object associated with the User object
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            user_profile.blood_type = form.cleaned_data['blood_type']
            user_profile.location = form.cleaned_data['location']
            user_profile.age = form.cleaned_data['age']
            user_profile.gender = form.cleaned_data['gender']
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.is_donor = form.cleaned_data['is_donor']
            user_profile.save()
            logger.debug(f"Profile was successfully updated by {request.user} at {datetime.datetime.now()} ") 
            #messages.success(request, 'Your profile was successfully updated!')
            return redirect('main:index')
    else:
        form = UpdateUserForm(initial={
            'username': user.username,
            'password': user.password,            
            'email': user.email,
            'blood_type': user_profile.blood_type,
            'location': user_profile.location,
            'age': user_profile.age,
            'gender': user_profile.gender,
            'phone_number': user_profile.phone_number,
            'is_donor': user_profile.is_donor
        })
    return render(request, 'main/update_user.html', {'form': form})


def login_view(request):
    """Login view."""
    form = AuthenticationForm()
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        # If the user is authenticated, log them in and redirect to the homepage
        if user is not None:
            login(request, user)
            logger.debug(f" User : {request.user} logged in at {datetime.datetime.now()} ") 
            #messages.success(request, 'logged in successfully.')
            return redirect('main:index')
        else:
            form.add_error(None, "Invalid Username or password")
    return render(request, 'main/user_login.html', {'form': form})


def logout_view(request):
    """Logout View"""
    logout(request)
    logger.debug(f"user : {request.user} logged out at {datetime.datetime.now()} ") 
    #åmessages.success(request, 'logged out successfully.')
    return redirect('main:index')

def register_user_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            logger.debug(f"User {request.user} Registered at {datetime.datetime.now()} ") 
            return redirect('main:index')
    else:
        form = RegistrationForm()
    return render(request, 'main/register_user.html', {'form': form})


# Create your views here.
def index(request):
    logger.debug("Index view ") 
    Appointment.objects.filter(user=request.user)
    appointments_1 = Appointment.objects.all()
    
    all_blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    blood_type_count = UserProfile.objects.filter(
        is_donor=True,
        user__appointment__is_donation=True,
        user__appointment__appointment_date__lt=timezone.now()
    ).values('blood_type').annotate(count=Count('blood_type'))
    
    blood_type_list = []
    for blood_type in all_blood_types:
        count = 0
        for bt in blood_type_count:
            if bt['blood_type'] == blood_type:
                count = bt['count']
                break
        blood_type_list.append({'blood_type': blood_type, 'count': count})

    return render(request, 'main/index.html', {'appointments': appointments_1, 'blood_type_count': blood_type_list, 'datetimenow':datetime.datetime.now().date()})