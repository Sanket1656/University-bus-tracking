from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def home(request):
    return render(request , 'control/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.full_name = form.cleaned_data['full_name']
            user.save()
            return redirect('control:dashboard')  # Redirect to login page after successful signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'control/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student:home')
        else:
            return render(request, 'control/login.html', {'error': 'Invalid credentials'})
    return render(request, 'control/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'control/dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('control:login')
