from typing import Any
from django import forms
from django.urls import reverse
from django.db.models import Min
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from core.models import Bike, FastServiceOrder, FreeOnlineAppointment, ManualServiceOrder, ServiceOrder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Layout, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField


class DateInput(forms.DateInput):
    input_type = 'date'


class ManualServiceOrderBaseForm(forms.ModelForm):
    
    class Meta:
        model = ManualServiceOrder
        fields = [
            "first_name", "last_name", 
            "email", "address", "phone_number", 
            "full_bike_title", "service_type", "date",
            "service_number", "assigned_staff", "status", "comment"
        ]
        labels = {
            "first_name": _("Ime"),
            "last_name": _("Priimek"),
            "email": _("Email"),
            "address": _("Naslov"),
            "phone_number": _("Telefonska številka"),
            "full_bike_title": _("Polno ime kolesa"),
            "service_type": _("Tip servisa"),
            "date": _("Datum servisa"),
            "service_number": _("Številka servisa"),
            "assigned_staff": _("Dodeljeni zaposleni"),
            "status": _("Status"),
            "comment": _("Opomba")
        }
        widgets = {
            "date": DateInput()
        }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['assigned_staff'].queryset = User.objects.filter(is_staff=True, is_superuser=False)


class ManualServiceOrderCreateForm(ManualServiceOrderBaseForm):
    
    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_class = 'form-floating'
        helper.layout = Layout(
            FloatingField('first_name'),
            FloatingField('last_name'),
            FloatingField('email'),
            FloatingField('address'),
            FloatingField('phone_number'),
            FloatingField('full_bike_title'),
            FloatingField('service_type'),
            'date',
            FloatingField('service_number'),
            FloatingField('assigned_staff'),
            FloatingField('status'),
            FloatingField('comment'),
            Div(
                Submit("submit", _("Ustvari"), css_class="btn-violet"),
                css_class='d-flex justify-content-center mt-3'
            )
        )
        return helper


class ManualServiceOrderUpdateForm(ManualServiceOrderBaseForm):
    
    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_class = 'form-floating'
        delete_url = reverse("core:delete_manual_service_order", kwargs={"service_order_id": self.instance.pk})
        delete_text = _("Izbriši")
        helper.layout = Layout(
            FloatingField('first_name'),
            FloatingField('last_name'),
            FloatingField('email'),
            FloatingField('address'),
            FloatingField('phone_number'),
            FloatingField('full_bike_title'),
            FloatingField('service_type'),
            'date',
            FloatingField('service_number'),
            FloatingField('assigned_staff'),
            FloatingField('status'),
            FloatingField('comment'),
            Div(
                Submit("submit", _("Posodobi"), css_class="btn-violet"),
                HTML(f'<a class="confirm-delete btn-violet btn text-white mx-3" href="{delete_url}">{delete_text}</a>'),
                css_class='d-flex justify-content-center mt-3',
            )
        )
        return helper

    
class FastServiceOrderBaseForm(forms.ModelForm):
    class Meta:
        model = FastServiceOrder
        fields = [
            "user", "bike", "date", "service_type", 
            "status", "service_number", "assigned_staff", 
            "comment"
        ]
        labels = {
            "user": _("Uporabnik"),
            "bike": _("Kolo"),
            "date": _("Datum servisa"),
            "service_type": _("Tip servisa"),
            "status": _("Status"),
            "service_number": _("Številka servisa"),
            "assigned_staff": _("Dodeljeni zaposleni"),
            "comment": _("Opomba")
        }
        widgets = {
            "date": DateInput()
        }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['assigned_staff'].queryset = User.objects.filter(is_staff=True, is_superuser=False)
        self.fields['user'].queryset = User.objects.filter(is_staff=False, is_superuser=False)


class FastServiceOrderCreateForm(FastServiceOrderBaseForm):
    
    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_class = 'form-floating'
        helper.layout = Layout(
            FloatingField('user'),
            FloatingField('bike'),
            'date',
            FloatingField('service_type'),
            FloatingField('status'),
            FloatingField('service_number'),
            FloatingField('assigned_staff'),
            FloatingField('comment'),
            Div(
                Submit("submit", _("Ustvari"), css_class="btn-violet"),
                css_class='d-flex justify-content-center mt-3'
            )
        )
        return helper


class FastServiceOrderUpdateForm(FastServiceOrderBaseForm):
    
    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_class = 'form-floating'
        delete_url = reverse("core:delete_fast_service_order", kwargs={"service_order_id": self.instance.pk})
        delete_text = _("Izbriši")
        helper.layout = Layout(
            FloatingField('user'),
            FloatingField('bike'),
            'date',
            FloatingField('service_type'),
            FloatingField('status'),
            FloatingField('service_number'),
            FloatingField('assigned_staff'),
            FloatingField('comment'),
            Div(
                Submit("submit", _("Posodobi"), css_class="btn-violet"),
                HTML(f'<a class="confirm-delete btn-violet btn text-white mx-3" href="{delete_url}">{delete_text}</a>'),
                css_class='d-flex justify-content-center mt-3',
                
            )
        )
        return helper

class BikeModelForm(forms.ModelForm):
    
    class Meta():
        model = Bike
        fields = [
            'brand', 'model', 'year', 'serial_number'
        ]
        labels = {
            'brand': 'Znamka',
            'model': 'Model',
            'year': 'Letnik',
            'serial_number': 'Serijska številka'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        bike = super().save(commit=False)
        if commit:
            bike.owner = self.user
            bike.save()
        return bike
    
    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_class = 'form-floating'
        helper.layout = Layout(
            FloatingField('brand'),
            FloatingField('model'),
            FloatingField('year'),
            FloatingField('serial_number'),
            Div(
                Submit("submit", _("Ustvari"), css_class="btn-violet"),
                css_class='d-flex justify-content-center mt-3'
            )
        )
        return helper


class FastServiceOrderReservationForm(forms.Form):
    
    service_type = forms.ChoiceField(label=_("Vrsta servisa"), choices=ServiceOrder.SERVICE_CHOICES)
    online_appointment = forms.ModelChoiceField(label=_("Termin"),queryset=FreeOnlineAppointment.objects.none())
    comment = forms.CharField(label=_("Opomba"), required=False, widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the next 4 lines of code set the online queryset to be one per date
        # this ensures that the users don't see the duplicate termins
        appointments = FreeOnlineAppointment.objects.values('date').annotate(min_id=Min('id'))
        appointment_ids = [appointment['min_id'] for appointment in appointments]
        unique_appointments = FreeOnlineAppointment.objects.filter(id__in=appointment_ids).order_by('date')
        self.fields["online_appointment"].queryset = unique_appointments
        
        if not self.fields["online_appointment"].queryset.exists():
            for field in self.fields:
                self.fields[field].disabled = True
    
    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_class = 'form-floating'
        helper.layout = Layout(
            FloatingField('online_appointment'),
            FloatingField('service_type'),
            FloatingField('comment'),
            Div(
                Submit("submit", _("Rezerviraj"), css_class="btn-violet"),
                css_class='d-flex justify-content-center mt-3'
            )
        )
        return helper
    
    def save(self, user: User, bike: Bike):
        service_order = FastServiceOrder(
            user=user,
            bike=bike,
            date=self.cleaned_data["online_appointment"].date,
            service_type=self.cleaned_data["service_type"],
            comment=self.cleaned_data["comment"]
        )
        service_order.save()
        
    


        