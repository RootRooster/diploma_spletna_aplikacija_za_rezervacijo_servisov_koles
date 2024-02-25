from django import forms

from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Layout, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

class ExtendedUserCreationForm(UserCreationForm):
    address = forms.CharField(max_length=100)
    phone_number = PhoneNumberField()
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name","email", "password1", "password2"]
        
        labels = {
            "username": _("Uporabniško ime"),
            "first_name": _("Ime"),
            "last_name": _("Priimek"),
            "email": _("E-pošta")
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        user.profile.address = self.cleaned_data["address"]
        user.profile.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = _("Geslo")
        self.fields["password2"].label = _("Ponovi geslo")
        self.fields["address"].label = _("Naslov")
        self.fields["phone_number"].label = _("Telefonska številka")
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_class = 'form-floating'
        helper.layout = Layout(
            FloatingField('username'),
            FloatingField('first_name'),
            FloatingField('last_name'),
            FloatingField('email'),
            FloatingField('password1'),
            FloatingField('password2'),
            FloatingField('address'),
            FloatingField('phone_number'),
            Div(
                Submit("submit", _("Ustvari račun"), css_class="btn-violet"),
                css_class='d-flex justify-content-center mt-3'
            )
        )
        return helper

class ChrispyAuthenticationForm(AuthenticationForm):
    
    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_class = 'form-floating'
        helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password'),
            Div(
                HTML(
                    '<p>Še nimaš računa? <a href="{% url "registration:create-account" %}" class="text-decoration-none">Ustvari račun!</a></p>'
                ),
            ),
            Div(
                Submit("submit", _("Prijava"), css_class="btn-violet"),
                css_class='d-flex justify-content-center mt-3'
            )
        )
        return helper