import time
import threading
import openrouteservice
from decimal import Decimal
from django.core.management.base import BaseCommand
from tracker.models import Bus, BusStops

# OpenRouteService API Key
ORS_API_KEY = "5b3ce3597851110001cf6248a74f17f39f964c4382a587217c2c7866"
client = openrouteservice.Client(key=ORS_API_KEY)

class Command(BaseCommand):
    help = "Simulates all buses moving along predefined stops concurrently"

    def move_bus_along_route(self, bus):
        """Continuously moves a bus along its route."""
        while True:  # Keep moving continuously
            route_stops = BusStops.objects.filter(routes=bus.route).order_by("id")

            if route_stops.count() < 2:
                print(f"Skipping {bus.name}, less than 2 stops.")
                time.sleep(5)  # Avoid rapid looping if no route
                continue

            for i in range(len(route_stops) - 1):
                start_stop = route_stops[i]
                end_stop = route_stops[i + 1]

                # Get actual road route
                try:
                    route_data = client.directions(
                        coordinates=[
                            [float(start_stop.longitude), float(start_stop.latitude)],
                            [float(end_stop.longitude), float(end_stop.latitude)]
                        ],
                        profile='driving-car',
                        format='geojson'
                    )
                except Exception as e:
                    print(f"Error fetching route for {bus.name}: {e}")
                    continue

                route_geometry = route_data['features'][0]['geometry']['coordinates']

                # Move along the route step by step
                for coord in route_geometry:
                    bus.longitude = Decimal(coord[0])  # Convert float to Decimal
                    bus.latitude = Decimal(coord[1])   # Convert float to Decimal
                    bus.save()
                    print(f"Bus {bus.name} moved to ({bus.latitude}, {bus.longitude})")
                    time.sleep(1)  # Smooth transition

    def handle(self, *args, **kwargs):
        buses = Bus.objects.all()
        threads = []

        for bus in buses:
            thread = threading.Thread(target=self.move_bus_along_route, args=(bus,), daemon=True)
            thread.start()
            threads.append(thread)

        print("All buses are now moving simultaneously!")

        while True:
            time.sleep(2)  # Keep the main process running
