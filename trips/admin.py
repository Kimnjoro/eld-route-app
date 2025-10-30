# trips/admin.py
from django.contrib import admin
from .models import Trip

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "pickup", "dropoff", "created_at", "cycle_used_hours")
    list_filter = ("created_at",)
    search_fields = ("pickup", "dropoff", "current_location")
