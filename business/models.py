from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now  # Import timezone
from users.models import CustomUser  # ✅ Correct

# modal for business 
class Business(models.Model):
    BUSINESS_TYPES = [
        ('online', 'Online'),
        ('physical', 'Physical'),
        ('both', 'Both'),
    ]

    ADDITIONAL_SERVICES = [
        ('home_delivery', 'Home Delivery'),
        ('free_wifi', 'Free Wi-Fi'),
        ('parking', 'Parking'),
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business', blank=True, null=True)  # ✅ ForeignKey
    business_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    contact_info = models.CharField(max_length=50)
    description = models.TextField()
    business_images = models.ImageField(upload_to='business_images/', blank=True, null=True)
    opening_hours = models.TimeField(blank=True, null=True)
    closing_hours = models.TimeField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    social_media = models.URLField(blank=True, null=True)
    business_type = models.CharField(max_length=10, choices=BUSINESS_TYPES)
    additional_services = models.TextField(blank=True, null=True)  # Simple text input for services
    business_reg_no = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.business_name

# ✅ New Model for Search History
class SearchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Stores searches for logged-in users
    session_id = models.CharField(max_length=255, null=True, blank=True)  # Stores searches for anonymous users
    category = models.CharField(max_length=255, null=True, blank=True)  # Stores searched categories
    query = models.CharField(max_length=255, null=True, blank=True)  # Stores searched text (address, pincode, etc.)
    timestamp = models.DateTimeField(auto_now_add=True)  # Saves the time of search

    def __str__(self):
        return f"{self.user} - {self.category} - {self.query} - {self.timestamp}"