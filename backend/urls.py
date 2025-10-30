from django.contrib import admin
from django.urls import path, re_path
from trips import views as trips_views
from backend.views import FrontendAppView  # import catch-all view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/trips/compute-route/", trips_views.compute_route, name="compute-route"),
    
    # Catch-all path for React frontend
    re_path(r'^.*$', FrontendAppView.as_view(), name='frontend'),
]
