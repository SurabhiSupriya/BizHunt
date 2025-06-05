from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Business, SearchHistory
from users.models import CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
import difflib

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
@login_required
def business_register(request):
    users = CustomUser.objects.filter(user_type='business')
    categories = Business.objects.values_list("category", flat=True).distinct()  # ✅ Dynamic categories

    if request.method == "POST":
        business = Business(
            owner=CustomUser.objects.get(id=request.POST.get("business_owner")),
            business_name=request.POST.get("business_name"),
            category=request.POST.get("category"),
            address=request.POST.get("address"),
            pincode=request.POST.get("pincode"),
            contact_info=request.POST.get("contact_info"),
            description=request.POST.get("description"),
            opening_hours=request.POST.get("opening_hours"),
            closing_hours=request.POST.get("closing_hours"),
            website=request.POST.get("website"),
            social_media=request.POST.get("social_media"),
            business_type=request.POST.get("business_type"),
            business_reg_no=request.POST.get("business_reg_no"),
            additional_services=request.POST.get("additional_services"),
            business_images=request.FILES.get("business_images"),
        )
        business.save()
        messages.success(request, f"Business '{business.business_name}' registered successfully!")
        return redirect("business_list")

    return render(request, "business_register.html", {"users": users, "categories": categories})

@login_required
def business_list(request):
    category = request.GET.get("category", "").strip()
    query = request.GET.get("query", "").strip()

    businesses = Business.objects.all().annotate(
        avg_rating=Avg("reviews__rating"),
        total_reviews=Count("reviews")
    )

    if category:
        businesses = businesses.filter(category__icontains=category)

    if query:
        businesses = businesses.filter(
            Q(pincode__icontains=query) |
            Q(address__icontains=query)
        )

    businesses = businesses.order_by('-avg_rating', '-total_reviews')

    if category or query:
        SearchHistory.objects.create(
            user=request.user,
            category=category if category else None,
            query=query if query else None
        )

    recommended_businesses = recommend_businesses(request.user)

    categories = Business.objects.values_list("category", flat=True).distinct()

    return render(request, "business_list.html", {
        "businesses": businesses,
        "categories": categories,
        "query": query,
        "selected_category": category,
        "recommended_businesses": recommended_businesses,
    })

def recommend_businesses(user):
    if not user.is_authenticated:
        return Business.objects.none()

    recent_searches = SearchHistory.objects.filter(user=user).order_by("-timestamp")[:5]

    recommended_businesses = Business.objects.none()

    for search in recent_searches:
        if search.category:
            recommended_businesses |= Business.objects.filter(category__icontains=search.category)
        if search.query:
            recommended_businesses |= Business.objects.filter(
                pincode__icontains=search.query
            ) | Business.objects.filter(address__icontains=search.query)

    return recommended_businesses.annotate(
        avg_rating=Avg("reviews__rating"),
        total_reviews=Count("reviews")
    ).order_by("-avg_rating", "-total_reviews").distinct()

@login_required
def smart_search_businesses(request):
    query = request.GET.get("q", "").strip()
    businesses = Business.objects.all()

    if query:
        all_names = Business.objects.values_list('business_name', flat=True)
        close_matches = difflib.get_close_matches(query, [name for name in all_names], n=5, cutoff=0.6)

        search_filter = (
            Q(business_name__icontains=query) |
            Q(category__icontains=query) |
            Q(address__icontains=query) |
            Q(pincode__icontains=query) |
            Q(additional_services__icontains=query)
        )

        if close_matches:
            search_filter |= Q(business_name__in=close_matches)

        businesses = businesses.filter(search_filter)

    businesses = businesses.annotate(
        avg_rating=Avg("reviews__rating"),
        total_reviews=Count("reviews")
    ).order_by('-avg_rating', '-total_reviews')

    return render(request, "smart_search.html", {
        "businesses": businesses,
        "query": query,
    })

@login_required
def live_search_suggestions(request):
    query = request.GET.get("q", "").strip()
    suggestions = []

    if query:
        businesses = Business.objects.filter(
            Q(business_name__icontains=query) |
            Q(category__icontains=query) |
            Q(address__icontains=query)
        ).values_list('business_name', flat=True)[:5]

        suggestions = list(businesses)

    return JsonResponse({'suggestions': suggestions})
