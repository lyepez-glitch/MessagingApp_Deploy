from django.urls import path

from . import views

urlpatterns = [
    path("", views.rooms, name="rooms"),
    path("signUp", views.signUp, name="signUp"),
    path("logIn", views.logIn, name="logIn"),
    path("logout/", views.logOut, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile", views.profile, name="profile"),
    path("message", views.message, name="message"),
    path("room/<int:user_id>/", views.room, name="room")
]