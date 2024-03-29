from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from django.db import models
from myLibrary.myAdminValidator import AdminValidation

class Clinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, validators=[AdminValidation.is_valid_phone])
    email = models.EmailField(validators=[AdminValidation.is_valid_email])
    contact_person = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField()

    def __str__(self):
        return self.name
        

class Bloodbank(models.Model):
    """Class for bloodbankProfile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username