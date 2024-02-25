from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("get/next/big", views.get_next_month_big, name="get_next_month_big"),
    path("get/previous/big", views.get_previous_month_big, name="get_previous_month_big"),
    path("get/current/big", views.get_current_month_big, name="get_current_month_big"),
    path("get/next/small", views.get_next_month_small, name="get_next_month_small"),
    path("get/previous/small", views.get_previous_month_small, name="get_previous_month_small"),
    path("get/current/small", views.get_current_month_small, name="get_current_month_small")
]