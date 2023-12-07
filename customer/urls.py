from django.urls import path
from customer.views import custom_login, custom_logout
from . import views

app_name = "customer"
urlpatterns = [
    path("", views.get_home_page, name="home_page"),
    path('signup/', views.signup, name='signup'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
]
