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

        Review.objects.create(
            name=name,
            message=message,
            rating=rating
        )

        send_mail(
            subject=f"📝 New Customer Review from {name}",
            message=f"""
New Review Submitted on JoTravels UK 🚕
Name: {name}
Rating: {rating}/5
Message: {message}

Please review it here:
https://jotravels.uk/admin/main/review/
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER, settings.CLIENT_EMAIL],
        )

        if email:
            send_mail(
                subject="🙏 Thank You for Your Review - JoTravels UK",
                message=f"""
Hi {name},

Thank you for sharing your experience with JoTravels UK! 🚕
We truly appreciate your feedback.

Warm regards,
JoTravels UK Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

        return render(request, 'reviews.html', {'success': True})

    reviews_list = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': reviews_list})


# ---------- Booking ----------
def booking(request):

    # Pass WhatsApp number always
    context = {
        "whatsapp_number": settings.WHATSAPP_NUMBER
    }

    if request.method == "POST":
        name = request.POST.get('name')
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        date_time = request.POST.get('date_time')
        phone = request.POST.get('phone')

        Booking.objects.create(
            name=name,
            pickup=pickup,
            drop=drop,
            date_time=date_time,
            phone=phone
        )

        # Email admin + client
        send_mail(
            subject=f"🚖 New Booking Request from {name}",
            message=f"""
New booking request received!

Name: {name}
Pickup: {pickup}
Drop: {drop}
Date & Time: {date_time}
Phone: {phone}

Approve this booking:
https://jotravels.uk/admin/main/booking/
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER, settings.CLIENT_EMAIL],
        )

        # WhatsApp message
        message = (
            f"🚖 JoTravels UK Booking Request:%0A"
            f"Name: {name}%0A"
            f"Pickup: {pickup}%0A"
            f"Drop: {drop}%0A"
            f"Date & Time: {date_time}%0A"
            f"Phone: {phone}"
        )

        whatsapp_link = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={message}"

        context["success"] = True
        context["whatsapp_link"] = whatsapp_link

    return render(request, 'booking.html', context)
