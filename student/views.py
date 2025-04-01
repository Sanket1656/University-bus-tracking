from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, StudentBusDetail
from .forms import StudentProfileForm, StudentBusDetailForm 
from tracker.models import DriverProfile , DriverBusDetail , BusAssignment 
from tracker.forms import DriverProfileForm , DriverBusDetailForm 
import requests, json

# Student Home View
@login_required
def student_home(request):
    bus_detail = None
    bus_assigned = None

    # Check if the user is a student
    try:
        bus_detail = StudentBusDetail.objects.get(student_name=request.user)
        bus_assigned = BusAssignment.objects.filter(students=request.user).first()
    except StudentBusDetail.DoesNotExist:
        pass  # No need to set bus_detail and bus_assigned again, as defaults are already set

    # Check if the user is a driver
    try:
        if not bus_detail:  # Avoid overwriting student details if already found
            bus_detail = DriverBusDetail.objects.get(driver=request.user)
            bus_assigned = BusAssignment.objects.filter(driver=request.user).first() 
    except DriverBusDetail.DoesNotExist:
        pass  # No bus details found for this user

   
      # Fetch only the assigned bus and its stops
    buses_json = []
    stops_json = []

    if bus_assigned:
        bus = bus_assigned.bus 
        buses_json = [{
            "id": bus.id,
            "name":bus.name,
            "route": bus.route.name,
            "latitude": float(bus.latitude),
            "longitude": float(bus.longitude),
        }]
        stops_json = [
            {"name": stop.name, "latitude": float(stop.latitude), "longitude": float(stop.longitude)}
            for stop in bus.route.bus_stops.all()
        ]
    


    return render(request, 'student/home.html', {
        'bus_detail': bus_detail,
        'bus_assigned': bool(bus_assigned),
        'buses_json': json.dumps(buses_json),
        'stops_json': json.dumps(stops_json),
    })





# Student Profile View
@login_required
def student_profile(request):
    if request.user.role == 'student':
        profile = StudentProfile.objects.get(user=request.user)
        return render(request, 'student/student_profile.html', {'profile': profile})
    else:
        return redirect('student:driver_profile')

# Edit Student Profile View
@login_required
def edit_student_profile_view(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student:student_profile')  # Redirect to the profile page
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'student/edit_profile.html', {'form': form})

@login_required
def edit_student_bus_detail_view(request):
    try:
        profile = StudentBusDetail.objects.get(student_name=request.user)
    except StudentBusDetail.DoesNotExist:
        profile = None
        
    if request.method == 'POST':
        form =StudentBusDetailForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student:bus_detail_view')  # Fixed redirect to bus detail view
    else:
        form = StudentBusDetailForm(instance=profile)

    return render(request, 'student/edit_bus_detail.html', {'form': form})

# Student and driver  Bus Detail View
@login_required
def bus_detail_view(request):
    if request.user.role == 'student':
        try:
            bus_assignment = BusAssignment.objects.filter(students=request.user).first()
        except BusAssignment.DoesNotExist:
            bus_assignment = None

        try:
            bus_detail = StudentBusDetail.objects.get(student_name=request.user)
        except StudentBusDetail.DoesNotExist:
            bus_detail = None

        if request.method == 'POST':
            form = StudentBusDetailForm(request.POST, instance=bus_detail)
            if form.is_valid():
                bus_detail = form.save()
                return redirect('student:bus_detail_view')
        else:
            form = StudentBusDetailForm(instance=bus_detail)

        return render(request, 'student/bus_detail_view.html', {
            'form': form,
            'bus_detail': bus_detail,
            'bus_assignment': bus_assignment,
            'filled': bus_detail is not None or bus_assignment is not None,
        })

    elif request.user.role == 'driver':
        try:
            bus_assignment = BusAssignment.objects.get(driver=request.user)
        except BusAssignment.DoesNotExist:
            bus_assignment = None

        try:
            bus_detail = DriverBusDetail.objects.get(driver=request.user)
        except DriverBusDetail.DoesNotExist:
            bus_detail = None

        if request.method == 'POST':
            form = DriverBusDetailForm(request.POST, instance=bus_detail)
            if form.is_valid():
                bus_detail = form.save()
                return redirect('student:bus_detail_view')
        else:
            form = DriverBusDetailForm(instance=bus_detail)
            
        print(f"DEBUG: request.user = {request.user} ({type(request.user)})")

        return render(request, 'driver/driver_bus_detail.html', {
            'form': form,
            'bus_detail': bus_detail,
            'bus_assignment': bus_assignment,
            'filled': bus_detail is not None or bus_assignment is not None,
        })

@login_required
def edit_driver_bus_detail_view(request):   
    try:
        profile = DriverBusDetail.objects.get(driver=request.user)
    except DriverBusDetail.DoesNotExist:
        profile = None  # Handle the case when no profile exists

    if request.method == 'POST':
        form = DriverBusDetailForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student:bus_detail_view')
    else:
        form = DriverBusDetailForm(instance=profile)

    return render(request, 'driver/edit_bus_detail.html', {'form': form, 'profile': profile})


@login_required
def driver_profile(request):
    if request.user.role == 'driver':
        profile = DriverProfile.objects.get(user=request.user)
        return render(request, 'driver/driver_profile.html', {'profile': profile})
    else:
        return redirect('student:student_profile')

@login_required
def edit_driver_profile_view(request):
    profile = DriverProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = DriverProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student:driver_profile')
    else:
        form = DriverProfileForm(instance=profile)

    return render(request, 'driver/edit_driver_profile.html', {'form': form})




import subprocess
import os
import signal
from django.http import JsonResponse

bus_process = None  # Store process globally

def start_bus_tracking(request):
    global bus_process
    if bus_process is None:
        bus_process = subprocess.Popen(["python", "manage.py", "move_bus"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return JsonResponse({"status": "started"})
    return JsonResponse({"status": "already running"})

def stop_bus_tracking(request):
    global bus_process
    if bus_process:
        bus_process.terminate()  # Terminate process safely
        bus_process.wait()  # Ensure process cleanup
        bus_process = None
        return JsonResponse({"status": "stopped"})
    return JsonResponse({"status": "not running"})
