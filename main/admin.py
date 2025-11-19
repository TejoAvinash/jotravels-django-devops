from django.contrib import admin
from .models import Booking, Review

# ----------------------------------
# REVIEW ADMIN
# ----------------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "message", "created_at", "approved")
    list_filter = ("approved", "rating", "created_at")
    search_fields = ("name", "message")
    ordering = ("-created_at",)

    actions = ["approve_reviews", "reject_reviews"]

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)

    @admin.action(description="Reject selected reviews")
    def reject_reviews(self, request, queryset):
        queryset.update(approved=False)


# ----------------------------------
# BOOKING ADMIN
# ----------------------------------
from django.utils.html import format_html

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "pickup", "drop", "date_time", "phone", "coloured_status")
    list_filter = ("status", "date_time")
    search_fields = ("name", "pickup", "drop", "phone")
    ordering = ("-date_time",)

    actions = ["mark_confirmed", "mark_cancelled", "mark_completed"]

    # 🔥 Coloured status badge
    def coloured_status(self, obj):
        color_map = {
            "pending": "orange",
            "confirmed": "green",
            "completed": "blue",
            "cancelled": "red",
        }
        color = color_map.get(obj.status, "black")
        return format_html(
            '<span style="padding:4px 7px; border-radius:5px; color:white; background:{};">{}</span>',
            color,
            obj.status.capitalize(),
        )

    coloured_status.short_description = "Status"

    # Actions
    @admin.action(description="Mark as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    @admin.action(description="Mark as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status="cancelled")

    @admin.action(description="Mark as Completed")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")

