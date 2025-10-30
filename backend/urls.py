from django.contrib import admin
from django.urls import path, include, re_path
from trips import views as trips_views
from backend.views import FrontendAppView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/trips/compute-route/", trips_views.compute_route, name="compute-route"),
    # catch-all for React routes
    re_path(r"^(?:.*)/?$", FrontendAppView.as_view(), name="home"),
]
