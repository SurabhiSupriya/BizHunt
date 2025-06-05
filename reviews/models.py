from django.db import models
from django.contrib.auth.models import User
from business.models import Business
from users.models import CustomUser

class Review(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use CustomUser instead of User
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Star ratings from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.business.business_name} ({self.rating}⭐)"
