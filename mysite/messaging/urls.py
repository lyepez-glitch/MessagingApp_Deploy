from django.urls import path

from . import views

urlpatterns = [
    path("", views.rooms, name="rooms"),
    path("signUp", views.signUp, name="signUp"),
    path("logIn", views.logIn, name="logIn"),
    path("logout/", views.logOut, name="logout"),
    path("dashboard", views.dashboard, name="dashboard")
]