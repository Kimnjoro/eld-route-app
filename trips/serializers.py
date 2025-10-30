# trips/serializers.py
from rest_framework import serializers
from .models import Trip

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
        read_only_fields = ("id", "created_at", "route_geojson", "route_summary", "eld_logs", "exported_pdf")
