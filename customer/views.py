from django.shortcuts import render, redirect, get_object_or_404
import random

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, ServiceLocationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ServiceLocation
from django.views.decorators.http import require_http_methods
from django.urls import reverse


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('customer:home_page')
    else:
        form = SignUpForm()
    return render(request, 'customer/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You have successfully logged in")
                return redirect('customer:home_page')
            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'customer/login.html')


@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('customer:login')


def get_home_page(request):
    return render(request, 'customer/home.html', {})


@login_required
def view_profile(request):
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email
    }
    return render(request, 'customer/profile_view.html', context)


@login_required
def service_locations(request):
    locations = ServiceLocation.objects.filter(
        user=request.user,
        is_active=True,
        )
    return render(request, 'customer/service_locations.html', {'locations': locations})


@login_required
def add_service_location(request):
    if request.method == 'POST':
        form = ServiceLocationForm(request.POST)
        if form.is_valid():
            service_location = form.save(commit=False)
            service_location.user = request.user
            service_location.save()
            return redirect('customer:service_locations')
    else:
        form = ServiceLocationForm()
    return render(request, 'customer/add_service_location.html', {'form': form})


@login_required
def delete_service_location(request, location_id):
    location = get_object_or_404(ServiceLocation, pk=location_id, user=request.user)
    if request.method == 'POST':
        location.is_active = False
        location.save()
        messages.success(request, 'Service location is deleted.')
        return redirect('customer:service_locations')
    return render(request, 'customer/delete_service_location.html', {'location': location})


@login_required
def get_random_chart(request):
    return render(request, 'customer/show_chart.html', context={
        'x_axis': 'Some random X axis',
        'y_axis': 'Some random Y axis',
        'labels': [random.randint(1, 10) for _ in range(10)],
        'values': [random.randint(10, 100) for _ in range(10)]
    })
