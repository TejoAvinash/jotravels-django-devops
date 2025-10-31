from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'rating')
    search_fields = ('name', 'message')
    ordering = ('-created_at',)

from .models import Review, Booking

admin.site.register(Booking)
