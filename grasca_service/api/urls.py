from django.urls import include, path
from . import views, json_api

urlpatterns = [
    path("calendar/", include(("django_calendar.urls", "django_calendar"), namespace="django_calendar")),
    path("create-new-free-appointment/", views.create_new_free_appointment, name="create_new_free_appointment"),
    path("api-bike-list/", json_api.get_bikes_of_user, name="api_bike_list"),
    path("api-personal-daily-calendar/", views.get_personal_daily_calander, name="api_personal_daily_calendar"),
    path("api-post-comments-and-return-staff-comments/", views.post_comments_and_return_staff_comments, name="api_post_comments_and_return_staff_comments"),
]
