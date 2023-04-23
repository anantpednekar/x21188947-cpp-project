from django import forms
from .models import Clinic
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Bloodbank

from django import forms
from .models import Clinic

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'address', 'phone_number', 'email', 'contact_person', 'description', 'website']
    
    def save(self, commit=True):
        clinic = super(ClinicForm, self).save(commit=False)
        clinic.name = self.cleaned_data['name']
        clinic.address = self.cleaned_data['address']
        clinic.phone_number = self.cleaned_data['phone_number']
        clinic.email = self.cleaned_data['email']
        clinic.contact_person = self.cleaned_data['contact_person']
        clinic.description = self.cleaned_data['description']
        clinic.website = self.cleaned_data['website']
        if commit:
            clinic.save()
        return clinic

class CreateAdminForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label='Phone Number'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')
    
    def save(self, commit=True):
        user = super(CreateAdminForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            bloodbank = Bloodbank.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user

class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


