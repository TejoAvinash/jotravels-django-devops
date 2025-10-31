from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Review, Booking

# ---------- Home Page ----------
def home(request):
    return render(request, 'home.html')

# ---------- About Page ----------
def about(request):
    return render(request, 'about.html')

# ---------- Reviews ----------
def reviews(request):
    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')
        rating = request.POST.get('rating')
        email = request.POST.get('email')

        new_review = Review.objects.create(
            name=name,
            message=message,
            rating=rating
        )

        # Send email to admin
        send_mail(
            subject=f"📝 New Customer Review from {name}",
            message=f"""
New Review Submitted on JoTravels UK 🚕
Name: {name}
Rating: {rating}/5
Message: {message}

Please review and approve it in the admin panel:
http://127.0.0.1:8000/admin/main/review/
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        # Send thank-you email to customer
        if email:
            send_mail(
                subject="🙏 Thank You for Your Review - JoTravels UK",
                message=f"""
Hi {name},

Thank you for sharing your experience with JoTravels UK! 🚕
We truly appreciate your feedback and hope to serve you again soon.

Warm regards,  
JoTravels UK Team  
Nottingham, United Kingdom
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

        return render(request, 'reviews.html', {'success': True})

    reviews = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': reviews})


# ---------- Booking ----------
def booking(request):
    if request.method == "POST":
        name = request.POST.get('name')
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        date_time = request.POST.get('date_time')
        phone = request.POST.get('phone')

        # Save booking in DB
        Booking.objects.create(
            name=name,
            pickup=pickup,
            drop=drop,
            date_time=date_time,
            phone=phone
        )

        # Send email to admin
        send_mail(
            subject=f"🚖 New Booking Request from {name}",
            message=f"""
New booking request received!

Name: {name}
Pickup: {pickup}
Drop: {drop}
Date & Time: {date_time}
Phone: {phone}

Approve this booking in admin panel:
http://127.0.0.1:8000/admin/main/booking/
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        # ✅ WhatsApp integration
        whatsapp_message = (
            f"🚖 JoTravels UK Booking Request:%0A"
            f"Name: {name}%0A"
            f"Pickup: {pickup}%0A"
            f"Drop: {drop}%0A"
            f"Date & Time: {date_time}%0A"
            f"Phone: {phone}"
        )
        whatsapp_link = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={whatsapp_message}"



        return render(request, 'booking.html', {
            'success': True,
            'whatsapp_link': whatsapp_link
        })

    return render(request, 'booking.html')
import os
print("Loaded Email:", os.getenv('EMAIL_HOST_USER'))
