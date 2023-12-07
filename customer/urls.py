from django.urls import path

from . import views

app_name = "customer"
urlpatterns = [
    path("", views.get_home_page, name="home_page"),
]
