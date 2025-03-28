from django.http import JsonResponse 
from .models import Bus, BusStops , BusAssignment ,DriverBusDetail , DriverProfile
from django.shortcuts import redirect , render ,get_object_or_404

def all_buse_view(request):
    buses = Bus.objects.all()
    return render(request , 'tracker/bus_veiw.html', {'buses': buses})

def bus_detail_view(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    bus_assignment = BusAssignment.objects.filter(bus=bus).first()
    
    if bus_assignment:
        stops = bus_assignment.bus_stops.all()
        driver = bus_assignment.driver  # This is a CustomUser object
        driver_name = driver.username if driver else "Not Assigned"
        
        # Get the driver's profile to access phone_number
        driver_profile = DriverProfile.objects.filter(user=driver).first() if driver else None
        driver_phone = driver_profile.phone_number if driver_profile else "N/A"
        driver_image_url = driver_profile.profile_picture.url if driver_profile and driver_profile.profile_picture else "https://via.placeholder.com/150"
    else:
        stops = []
        driver_name = "Not Assigned"
        driver_phone = "N/A"
        driver_image_url = "https://via.placeholder.com/150"

    return render(request, 'tracker/bus_detail.html', {
        'bus': bus,
        'stops': stops,
        'driver_name': driver_name,
        'driver_phone': driver_phone,
        'driver_image_url': driver_image_url,
    })



def get_bus_locations(request):
    buses = Bus.objects.all()
    bus_data = [
        {
            "name": bus.name,
            "latitude": float(bus.latitude),  
            "longitude": float(bus.longitude),  
            "route": bus.route.name,
        }
        for bus in buses
    ]
    return JsonResponse(bus_data, safe=False)

def get_bus_stops(request):
    stops = BusStops.objects.all()
    stop_data = [
        {
            "name": stop.name,
            "latitude": float(stop.latitude),  
            "longitude": float(stop.longitude),     
        }
        for stop in stops
    ]
    return JsonResponse(stop_data, safe=False)

