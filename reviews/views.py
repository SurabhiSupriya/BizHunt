from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from business.models import Business
from .models import Review

@login_required
def add_review(request, business_id):
    business = get_object_or_404(Business, id=business_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if rating and comment:
            Review.objects.create(
                business=business,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            return redirect("business_list")  # ✅ Go back to business list after review

    return render(request, "add_review.html", {"business": business})

def business_reviews(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    reviews = business.reviews.all()

    return render(request, "business_reviews.html", {"business": business, "reviews": reviews})
