from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now  # Import timezone

# model for users 
class CustomUser(AbstractUser):
    SIGNUP_CHOICES = [
        ('user', 'User'),
        ('business', 'Business Owner'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    user_type = models.CharField(max_length=8, choices=SIGNUP_CHOICES, default='user')  # ✅ FIXED max_length

    # Business Owner Fields
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)

    # Fix conflicting fields
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return self.username

