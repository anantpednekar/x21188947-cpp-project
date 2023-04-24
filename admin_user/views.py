import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Count


from .forms import AdminLoginForm, ClinicForm, CreateAdminForm
from .models import Bloodbank, Clinic
from main.models import UserProfile

@login_required
def clinic_delete(request, pk):
    #messages.success(request, 'Recipe deleted successfully.')
    clinic = get_object_or_404(Clinic, pk=pk)
    clinic.delete()
    return redirect('admin_user:admin_home')


def admin_logout(request):
    """Logout View"""
    logout(request)
    #åmessages.success(request, 'logged out successfully.')
    return redirect('main:index')

@login_required
def admin_register(request):
    if request.method == 'POST':
        form = CreateAdminForm(request.POST)
        if form.is_valid():
            bloodbank = form.save(commit=False)
            bloodbank.user = request.user
            bloodbank.save()
            messages.success(request, 'Your bloodbank profile has been created!')
            return redirect('admin_user:admin_home')
    else:
        form = CreateAdminForm()
    return render(request, 'admin_user/admin_register.html', {'form': form})


def admin_login(request):
    """View for blood bank login."""
    form = AdminLoginForm()
    if request.method == 'POST':
        # Get the email and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        # If the user is authenticated, log them in and redirect to the homepage
        if user is not None:
            if username == 'admin2' and password == 'AAAA1111DDDD':
                login(request, user)
                return redirect('admin_user:admin_home')
        else:
            form.add_error(None, "Invalid username or password.")
    return render(request, 'admin_user/admin_login.html', {'form': form})


@login_required
def create_clinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_user:admin_home')
    else:
        form = ClinicForm()
    return render(request, 'admin_user/create_clinic.html', {'form': form})

@login_required
def admin_home(request):
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

    clinics = Clinic.objects.all()
    return render(request, 'admin_user/admin_home.html', {'clinics': clinics, 'blood_type_count': blood_type_list})
    

