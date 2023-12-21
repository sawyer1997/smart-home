from django.shortcuts import get_object_or_404
import random

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, ServiceLocationForm, ProfileEditForm, ServiceLocationUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ServiceLocation
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
            messages.success(request, "Successfully signed up and logged you in!")
            return redirect('customer:home_page')
    else:
        form = SignUpForm()
    return render(request, 'customer/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.raw('SELECT * FROM auth_user WHERE username = %s', [username])

        if len(user):
            user = user[0]
        else:
            messages.error(request, "No account found with that username. Please register.")
            return redirect('customer:home_page')

        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is inactive.")
                return redirect('customer:login')

            if not user.check_password(password):
                messages.error(request, "Incorrect Password! Please try again. ")
                return redirect('customer:login')

            user = authenticate(request, username=username, password=password)
            if user.is_active:
                login(request, user)
                messages.success(request, "You have successfully logged in")
                return redirect('customer:home_page')
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
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile successfully updated.")
            return redirect(reverse('customer:view_profile'))
    else:
        profile_form = ProfileEditForm(instance=user)
    return render(request, 'customer/edit_profile.html', context={'form': profile_form})


@login_required
def milestone_profile(request):
    if request.method == 'POST':
        try:
            current_user = User.objects.raw('SELECT * FROM auth_user WHERE id = %s', [request.user.id])[0]
            if current_user.is_active:
                current_user.is_active = False
                current_user.save()
                logout(request)
                messages.success(request, "Successfully deleted your profile!")
            return redirect(reverse('customer:home_page'))
        except Exception as e:
            print(e)
    return render(request, 'customer/delete_profile.html')


# ============================ SERVICE LOCATION IMPLEMENTATION ======================================


@login_required
def service_locations(request):
    sql_query = (
        f"SELECT * FROM customer_servicelocation "
        f"WHERE user_id = {request.user.id} AND is_active = 't'"
    )
    locations = ServiceLocation.objects.raw(sql_query)
    return render(request, 'customer/view_locations.html', {'locations': locations})


@login_required
def detailed_service_locations(request):
    location_id = request.POST.get('location_id')
    sql_query = (f"SELECT * from customer_servicelocation "
                 f"WHERE id = {location_id}")
    locations = ServiceLocation.objects.raw(sql_query)
    if len(locations) == 0:
        return redirect(reverse('customer:service_locations'))
    location = locations[0]
    return render(request, 'customer/service_locations.html', {'location': location})


@login_required
def add_service_location(request):
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
def update_service_location(request, location_id):
    sl_instance = ServiceLocation.objects.raw(
        f"SELECT * from customer_servicelocation WHERE id = {location_id}"
    )
    if len(sl_instance) == 0:
        messages.error(request, "No location found!")
        return redirect(reverse('customer:service_locations'))
    sl_instance = sl_instance[0]
    if sl_instance.user != request.user:
        messages.error(request, 'You do not have permission to update this!')
        return redirect(reverse('customer:service_locations'))
    if request.method == 'POST':
        sl_form = ServiceLocationUpdateForm(request.POST, instance=sl_instance)
        if sl_form.is_valid():
            sl_form.save()
            messages.success(request, 'Service location details updated successfully')
            return redirect('customer:service_locations')
    sl_form = ServiceLocationUpdateForm(instance=sl_instance)
    return render(request, 'customer/update_location.html', {'sl_form': sl_form})


@login_required
def delete_service_location(request, location_id):
    location = get_object_or_404(ServiceLocation, pk=location_id, user=request.user)
    if location.user != request.user:
        messages.error(request, 'You do not have permission to delete this!')
        return redirect(reverse('customer:service_locations'))
    if request.method == 'POST':
        location.is_active = False
        location.save()
        messages.success(request, 'Service location is deleted.')
        return redirect('customer:service_locations')
    return render(request, 'customer/delete_service_location.html', {'location': location})


@login_required
def get_random_chart(request):
    labels = [f'Category {i}' for i in range(10)]
    return render(request, 'customer/show_piechart.html', context={
        'x_axis': 'Some random X axis',
        'y_axis': 'Some random Y axis',
        'labels': labels,
        'values': [random.randint(10, 100) for _ in range(10)],
        'data': [random.randint(10, 100) for _ in range(10)],
    })
