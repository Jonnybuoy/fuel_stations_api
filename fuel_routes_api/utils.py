import logging
import os
import requests

from geopy.distance import geodesic

maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
maps_api_url = os.getenv("GOOGLE_MAPS_API_URL")

def geocode_address(address):
    """Geocode an address using the Google Maps API."""
    url = f"{maps_api_url}/geocode/json?address={address}&key={maps_api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

def get_route(start, end):
    """Get the route between start and end locations."""
    url = f"{maps_api_url}/directions/json?origin={start}&destination={end}&key={maps_api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        route_points = []
        steps = data['routes'][0]['legs'][0]['steps']
        for step in steps:
            route_points.append(step['start_location'])
        route_points.append(steps[-1]['end_location'])
        return route_points
    return []

def calculate_fuel_stops(route_points, fuel_stations, max_range=500, mpg=10):
    """
    Calculate optimal fuel stops along the route.

    Args:
        route_points (list): List of (latitude, longitude) tuples for the route.
        fuel_stations (QuerySet): QuerySet of FuelStation objects.
        max_range (int): Maximum range of the vehicle in miles.
        mpg (int): Miles per gallon for the vehicle.

    Returns:
        tuple: (list of selected stations, total cost)
    """
    stops = []
    total_cost = 0
    remaining_range = max_range
    gallons_needed = max_range / mpg 
    route_points = [(point['lat'], point['lng']) for point in route_points]

    for i in range(len(route_points) - 1):
        start_point = route_points[i]
        next_point = route_points[i + 1]
        segment_distance = geodesic(start_point, next_point).miles

        # Reduce the remaining range
        remaining_range -= segment_distance

        # If remaining range is below a threshold, find the nearest, cheapest station
        if remaining_range <= 100:  # Buffer to avoid running out of fuel
            nearby_stations = [
                station for station in fuel_stations
                if geodesic((station.latitude, station.longitude), start_point).miles <= max_range
            ]

            if not nearby_stations:
                raise ValueError("No fuel stations found within range.")

            # Select the cheapest nearby station
            cheapest_station = min(nearby_stations, key=lambda s: s.retail_price)
            stops.append(cheapest_station)

            # Calculate cost for refueling
            total_cost += gallons_needed * cheapest_station.retail_price
            remaining_range = max_range  # Reset range after refueling

    return stops, total_cost


def generate_static_map(route_points, stops):
    """Generate a static map url."""
    # Generate the polyline path for the route points
    path = "|".join(f"{p['lat']},{p['lng']}" for p in route_points)
    
    # Generate markers for the fuel stops
    markers = "|".join(f"label:{i+1}|{s.latitude},{s.longitude}" for i, s in enumerate(stops))
    
    # Construct the static map URL
    base_url = f"{maps_api_url}/staticmap"
    params = {
        "size": "800x600",
        "path": f"color:0x0000ff|weight:5|{path}",
        "markers": markers,
        "key": maps_api_key
    }
    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base_url}?{query_string}"

