from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.ChrispyLoginView.as_view(), name="login"),
    path("create-account/", views.CreateNewUserFormView.as_view(), name="create-account"),
    path ("logout/", views.LogoutView.as_view(), name="logout")
]