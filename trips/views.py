import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.cache import cache  # ✅ For caching results

@api_view(['POST'])
def compute_route(request):
    try:
        current_location = request.data.get("current_location")
        pickup_location = request.data.get("pickup_location")
        dropoff_location = request.data.get("dropoff_location")
        cycle_hours = float(request.data.get("cycle_hours", 0))

        if not all([current_location, pickup_location, dropoff_location]):
            return JsonResponse({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Cache key to identify same route requests
        cache_key = f"route_{pickup_location}_{dropoff_location}_{cycle_hours}"
        cached_result = cache.get(cache_key)
        if cached_result:
            print("✅ Using cached route data.")
            return JsonResponse(cached_result, status=status.HTTP_200_OK)

        # ✅ Use OpenStreetMap Nominatim API for geocoding
        def geocode(location):
            res = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": location, "format": "json"},
                headers={"User-Agent": "Django-ELD-App"}
            )
            data = res.json()
            if not data:
                return None
            return float(data[0]["lat"]), float(data[0]["lon"])

        pickup_coords = geocode(pickup_location)
        dropoff_coords = geocode(dropoff_location)

        if not pickup_coords or not dropoff_coords:
            return JsonResponse({"error": "Could not find one or more locations"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Calculate approximate distance & time
        distance_km = ((pickup_coords[0] - dropoff_coords[0]) ** 2 + (pickup_coords[1] - dropoff_coords[1]) ** 2) ** 0.5 * 111
        hours = round(distance_km / 60, 2)
        remaining_hours = max(0, cycle_hours - hours)

        result = {
            "pickup": pickup_location,
            "dropoff": dropoff_location,
            "distance_km": round(distance_km, 2),
            "estimated_hours": hours,
            "remaining_cycle_hours": remaining_hours,
            "pickup_coords": pickup_coords,
            "dropoff_coords": dropoff_coords,
            "status": "success",
        }

        # ✅ Store in cache for faster future access (1 hour)
        cache.set(cache_key, result, timeout=3600)

        return JsonResponse(result, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ Error:", e)
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
