from django.shortcuts import render, redirect
from .forms import ClinicForm

from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .forms import AdminLoginForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateAdminForm
from .models import Bloodbank,Clinic

from django.shortcuts import get_object_or_404, redirect, render
from .models import Clinic

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
        if username == 'admin2' and password == 'AAAA1111DDDD':
            login(request, user)
            return redirect('admin_user:admin_home')
        else:
            form.add_error(None, "Invalid username or password.")
    return render(request, 'admin_user/admin_login.html', {'form': form})


def create_clinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_user:admin_home')
    else:
        form = ClinicForm()
    return render(request, 'admin_user/create_clinic.html', {'form': form})





def admin_home(request):
    clinics = Clinic.objects.all()
    return render(request, 'admin_user/admin_home.html', {'clinics': clinics})
    

