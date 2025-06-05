from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from business.models import Business
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        address = request.POST['address']
        gender = request.POST['gender']
        signup_type = request.POST.get('signup_type', 'user')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        business_name = request.POST.get('business_name', '')
        business_address = request.POST.get('business_address', '')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            contact_number=contact_number,
            address=address,
            gender=gender,
            user_type=signup_type,
            password=password
        )

        if signup_type == 'business':
            user.business_name = business_name
            user.business_address = business_address
            user.save()

            Business.objects.create(
                owner=user,
                business_name=business_name,
                address=business_address,
            )

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def index(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about_us.html')

@login_required
def profile(request):
    user = request.user
    business = None

    if user.user_type == 'business':
        business = Business.objects.filter(owner=user).first()

    return render(request, 'profile.html', {'user': user, 'business': business})

@login_required
def edit_profile(request):
    user = request.user
    business = None

    if user.user_type == "business":
        business = Business.objects.filter(owner=user).first()

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.contact_number = request.POST.get("contact_number", user.contact_number)
        user.address = request.POST.get("address", user.address)

        if "profile_image" in request.FILES:
            user.profile_image = request.FILES["profile_image"]

        user.save()

        if business:
            business.business_name = request.POST.get("business_name", business.business_name)
            business.category = request.POST.get("category", business.category)
            business.contact_info = request.POST.get("business_contact", business.contact_info)
            business.website = request.POST.get("business_website", business.website)

            if "business_image" in request.FILES:
                business.business_images = request.FILES["business_image"]  # ✅ Correctly assign uploaded file

            business.save()

        messages.success(request, "Profile updated successfully!")  # ✅ Popup message
        return redirect("profile")

    return render(request, "edit_profile.html", {"business": business, "user": user})

# ✅ Added Privacy Policy View
def privacy_policy(request):
    return render(request, 'privacy_policy.html')
