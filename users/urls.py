from django.contrib import admin
from django.urls import path, include
from users.views import signup, user_login, user_logout, index, about_us, profile, edit_profile, privacy_policy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('about_us/', about_us, name='about_us'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),

    # ✅ Business URLs
    path('business/', include('business.urls')),
]
