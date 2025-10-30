# trips/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
try:
    # Django 3.1+ has JSONField
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

User = get_user_model()

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    current_location = models.CharField(max_length=255)
    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255)
    cycle_used_hours = models.FloatField(default=0.0)

    route_geojson = JSONField(null=True, blank=True)
    route_summary = JSONField(null=True, blank=True)
    eld_logs = JSONField(null=True, blank=True)  # list of generated per-day logs
    exported_pdf = models.FileField(upload_to="eld_pdfs/", null=True, blank=True)

    def __str__(self):
        return f"Trip #{self.pk} {self.pickup} → {self.dropoff}"
