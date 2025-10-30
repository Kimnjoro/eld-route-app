from django.urls import path
from .views import compute_route

urlpatterns = [
    path("compute-route/", compute_route, name="compute-route"),
]
