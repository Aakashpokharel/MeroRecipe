from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    is_vendor = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False, null=True)
    """profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )"""
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
