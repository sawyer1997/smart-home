from django.urls import path
from . import views

app_name = "customer"
urlpatterns = [
    path("", views.get_home_page, name="home_page"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.view_profile, name='view_profile')
]
