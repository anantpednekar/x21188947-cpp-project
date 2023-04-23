from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

from django.forms.widgets import DateInput, TimeInput
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['clinic', 'appointment_date', 'appointment_time', 'is_donation']
        widgets = {
            'appointment_date': DateInput(attrs={'type': 'date'}),
            'appointment_time': TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'is_donation': 'Are you donating blood during this appointment?',
        }

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    BLOOD_TYPES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    blood_type = forms.ChoiceField(choices=BLOOD_TYPES)

    location = forms.CharField(required=True)
    age = forms.IntegerField(required=True)
    gender = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    is_donor = forms.BooleanField(required=False, label='Are you willing to be a blood donor?')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                blood_type=self.cleaned_data['blood_type'],
                location=self.cleaned_data['location'],
                age=self.cleaned_data['age'],
                gender=self.cleaned_data['gender'],
                phone_number=self.cleaned_data['phone_number'],
                is_donor=self.cleaned_data['is_donor']
            )
            profile.save()
        return user


class UpdateUserForm(forms.ModelForm):
    BLOOD_TYPES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )

    email = forms.EmailField(required=True)
    blood_type = forms.ChoiceField(choices=BLOOD_TYPES)
    location = forms.CharField(required=True)
    age = forms.IntegerField(required=True)
    gender = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    is_donor = forms.BooleanField(required=False, label='Are you willing to be a blood donor?')

    class Meta:
        model = User
        fields = ['username','password', 'email', 'blood_type', 'location', 'age', 'gender', 'phone_number', 'is_donor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['password'].disabled = True
        self.fields['password'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = user.userprofile
            profile.blood_type = self.cleaned_data['blood_type']
            
            profile.location = self.cleaned_data['location']
            profile.age = self.cleaned_data['age']
            profile.gender = self.cleaned_data['gender']
            profile.phone_number = self.cleaned_data['phone_number']
            profile.is_donor = self.cleaned_data['is_donor']
            profile.save()
        return user

