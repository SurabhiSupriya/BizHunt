from django.urls import path
from .views import add_review, business_reviews

urlpatterns = [
    path("add/<int:business_id>/", add_review, name="add_review"),
    path("business/<int:business_id>/reviews/", business_reviews, name="business_reviews"),
]
