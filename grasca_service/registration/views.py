from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from .forms import ChrispyAuthenticationForm, ExtendedUserCreationForm

class CreateNewUserFormView(CreateView):
    template_name = "registration/create_account.html"
    form_class = ExtendedUserCreationForm
    success_url = reverse_lazy('registration:login')

class ChrispyLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = ChrispyAuthenticationForm
    success_url = "/"

class LogoutView(RedirectView):
    url = reverse_lazy('home:home_page')
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
    
    
    
    