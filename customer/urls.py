from django.urls import path
from . import views

app_name = "customer"
urlpatterns = [
    path("", views.get_home_page, name="home_page"),

    path('signup/', views.signup, name='signup'),

    path('login/', views.custom_login, name='login'),

    path('logout/', views.custom_logout, name='logout'),

    path('profile/', views.view_profile, name='view_profile'),

    path('service_locations/', views.service_locations, name='service_locations'),

    path('detail_sl/', views.detailed_service_locations, name='detailed_service_locations'),

    path('add_service_location/', views.add_service_location, name='add_service_location'),

    path('delete_service_location/<int:location_id>/',
         views.delete_service_location, name='delete_service_location'),

    path('random_chart/', views.get_random_chart, name='random_chart'),

    path('delete_profile/', views.milestone_profile, name="milestone_profile"),

    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('edit_sl/<int:location_id>/', views.update_service_location, name="update_service_location"),
]
