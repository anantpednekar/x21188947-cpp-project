from django.db import models
from django.contrib.auth.models import User
from admin_user.models import Clinic
from django.core.validators import MinLengthValidator, EmailValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from myLibrary.myMainValidator import MainValidation

class UserProfile(models.Model):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    location = models.CharField(max_length=255)
    age = models.IntegerField(validators=[MainValidation.is_valid_age])
    gender = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, validators=[MainValidation.is_valid_phone])
    is_donor = models.BooleanField(default=False)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    is_donation = models.BooleanField(default=False)

