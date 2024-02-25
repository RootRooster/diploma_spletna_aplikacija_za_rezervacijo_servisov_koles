from typing import Any
from django import forms
from django.db.models import Min
from django.utils.translation import gettext as _
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField
from core.models import FreeOnlineAppointment, ServiceOrder

class QuickServiceForm(forms.Form):
    first_name = forms.CharField(label=_("Ime"), max_length=50)
    last_name = forms.CharField(label=_("Priimek"), max_length=50)
    email = forms.EmailField(label=_("Email"))
    full_bike_title = forms.CharField(label=_("Podaki o kolesu"), max_length=100, help_text=_("(znamka, model, letnik)"))
    address = forms.CharField(max_length=100, label=_("Naslov"))
    phone_number = PhoneNumberField(label=_("Telefonska"))
    service_type = forms.ChoiceField(label=_("Vrsta servisa"), choices=ServiceOrder.SERVICE_CHOICES)
    online_appointment = forms.ModelChoiceField(label=_("Termin"),queryset=FreeOnlineAppointment.objects.none())
    phone_number.error_messages['invalid'] = _("Napačen zapis telefonske številke")
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
            FloatingField('first_name'),
            FloatingField('last_name'),
            FloatingField('email'),
            FloatingField('address'),
            FloatingField('phone_number'),
            FloatingField('full_bike_title'),
            FloatingField('service_type'),
            FloatingField('online_appointment'),
            FloatingField('comment'),
            Div(
                Submit("submit", _("Oddaj"), css_class="btn-violet"),
                css_class='d-flex justify-content-center mt-3'
            )
        )
        return helper
        
        
    
