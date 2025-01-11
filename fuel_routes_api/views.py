from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import FuelStation
from .serializers import FuelStationSerializer
from .utils import (
    get_route, 
    generate_static_map, 
    calculate_fuel_stops
    )

# Create your views here.
class RouteView(View):
    def get(self, request):
        start = request.GET.get("start")
        end = request.GET.get("end")

        if not start or not end:
            return JsonResponse({"error": "Start and end locations are required."}, status=400)

        # Fetch the route
        route_points = get_route(start, end)

        # Fetch fuel stations
        fuel_stations = FuelStation.objects.all()

        # Calculate fuel stops
        stops, total_cost = calculate_fuel_stops(route_points, fuel_stations)

        serializer = FuelStationSerializer(stops, many=True)

        # Generate static map
        map_url = generate_static_map(route_points, stops)

        # Prepare response
        response = {
            "map_url": map_url,
            "fuel_stops": serializer.data,
            "total_fuel_cost": total_cost
        }

        return JsonResponse(response)
