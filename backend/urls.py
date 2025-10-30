# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from trips import views as trips_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/trips/compute-route/", trips_views.compute_route, name="compute-route"),
    # add more API endpoints under /api/ later
]
