from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home_page_view, name="home_page"),
    path("staff/", views.staff_home_page_view, name="staff_home_page"),
    path("profile/", views.profile_home_page_view, name="profile_home_page"),
]