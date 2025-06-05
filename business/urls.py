from django.urls import path
from business.views import business_register, business_list, smart_search_businesses, live_search_suggestions

urlpatterns = [
    path('business_register/', business_register, name='business_register'),
    path('business_list/', business_list, name='business_list'),
    path('smart_search/', smart_search_businesses, name='smart_search'),
    path('live_search/', live_search_suggestions, name='live_search'),  # ✅ For live suggestions
]
