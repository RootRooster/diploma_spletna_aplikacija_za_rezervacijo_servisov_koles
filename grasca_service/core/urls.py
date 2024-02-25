from django.contrib import admin
from django.urls import include, path
from core import views

urlpatterns = [
    path("create-new-manual-service-order/", views.ManualServiceOrderCreateView.as_view(), name="create_new_manual_service_order"),
    path("edit-manual-service-order/<int:service_order_id>/", views.ManualServiceOrderUpdateView.as_view(), name="edit_manual_service_order"),
    path("delete-manual-service-order/<int:service_order_id>/", views.ManualServiceOrderDeleteView.as_view(), name="delete_manual_service_order"),
    path("create-new-fast-service-order/", views.FastServiceOrderCreateView.as_view(), name="create_new_fast_service_order"),
    path("edit-fast-service-order/<int:service_order_id>/", views.FastServiceOrderUpdateView.as_view(), name="edit_fast_service_order"),
    path("delete-fast-service-order/<int:service_order_id>/", views.FastServiceOrderDeleteView.as_view(), name="delete_fast_service_order"),
    path("register-a-new-bike", views.UserBikeCreateView.as_view(), name="register_a_new_bike"),
    path("bike-history/<int:bike_id>/", views.BikeHistoryView.as_view(), name="bike_history"),
    path("fast-service-order-reservation/<int:bike_id>/", views.FastServiceOrderReservationView.as_view(), name="fast_service_order_reservation"),
    path("fast-service-order-detials/<int:service_order_id>/", views.FastServiceOrderDetailsView.as_view(), name="fast_service_order_details"),
    path("manual-service-order-details/<int:service_order_id>/", views.ManualServiceOrderDetailsView.as_view(), name="manual_service_order_details"),
]