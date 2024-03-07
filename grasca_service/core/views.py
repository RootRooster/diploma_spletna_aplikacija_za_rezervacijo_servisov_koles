from typing import Any
from datetime import date
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from core.models import Bike, FastServiceOrder, ManualServiceOrder, ManualServiceOrderStaffComment, FastServiceOrderStaffComment
from core.forms import BikeModelForm, ManualServiceOrderCreateForm, FastServiceOrderCreateForm, ManualServiceOrderUpdateForm, \
    FastServiceOrderUpdateForm, FastServiceOrderReservationForm
from core.mixins import StaffRequiredSuccessMessageMixin, RegularUserRequiredSuccessMessageMixin, RegularUserRequiredMixin
from django.utils.translation import gettext as _

from django_calendar.helpers import create_calendar_data, get_current_month_and_year


class ManualServiceOrderCreateView(StaffRequiredSuccessMessageMixin, CreateView):
    model = ManualServiceOrder
    form_class = ManualServiceOrderCreateForm
    success_url = reverse_lazy('home:staff_home_page')
    success_message = _("Naročilo uspešno ustvarjeno.")
    template_name = 'core/manual_service_order_form.html'

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        year = self.request.GET.get("year")
        month = self.request.GET.get("month")
        day = self.request.GET.get("day")
        if year and month and day:
            year, month, day = int(year), int(month), int(day)
            initial["date"] = date(year, month, day)
        return initial


class ManualServiceOrderUpdateView(StaffRequiredSuccessMessageMixin, UpdateView):
    model = ManualServiceOrder
    form_class = ManualServiceOrderUpdateForm
    pk_url_kwarg = "service_order_id"
    template_name = 'core/manual_service_order_form.html'
    success_message = _("Naročilo uspešno posodobljeno.")
    success_url = reverse_lazy('home:staff_home_page')


class ManualServiceOrderDeleteView(StaffRequiredSuccessMessageMixin, DeleteView):
    model = ManualServiceOrder
    pk_url_kwarg = "service_order_id"
    success_message = _("Naročilo uspešno odstranjeno.")
    success_url = reverse_lazy('home:staff_home_page')


class FastServiceOrderCreateView(StaffRequiredSuccessMessageMixin, CreateView):
    model = FastServiceOrder
    form_class = FastServiceOrderCreateForm
    success_url = reverse_lazy('home:staff_home_page')
    success_message = _("Naročilo uspešno ustvarjeno.")
    template_name = 'core/fast_service_order_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        year = self.request.GET.get("year")
        month = self.request.GET.get("month")
        day = self.request.GET.get("day")
        if year and month and day:
            year, month, day = int(year), int(month), int(day)
            initial["date"] = date(year, month, day)
        return initial


class FastServiceOrderUpdateView(StaffRequiredSuccessMessageMixin, UpdateView):
    model = FastServiceOrder
    form_class = FastServiceOrderUpdateForm
    pk_url_kwarg = "service_order_id"
    template_name = 'core/fast_service_order_form.html'
    success_url = reverse_lazy('home:staff_home_page')
    success_message = _("Naročilo uspešno posodobljeno.")


class FastServiceOrderDeleteView(StaffRequiredSuccessMessageMixin, DeleteView):
    model = FastServiceOrder
    pk_url_kwarg = "service_order_id"
    success_message = _("Naročilo uspešno odstranjeno.")
    success_url = reverse_lazy('home:staff_home_page')


class UserBikeCreateView(RegularUserRequiredSuccessMessageMixin, CreateView):
    model = Bike
    form_class = BikeModelForm
    template_name = 'core/bike_create_form.html'
    success_message = _("Kolo uspešno dodano.")
    success_url = reverse_lazy('home:staff_home_page')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class BikeHistoryView(RegularUserRequiredMixin, ListView):
    model = FastServiceOrder
    template_name = 'core/bike_history.html'
    
    def get_queryset(self):
        return FastServiceOrder.objects.filter(bike_id=self.kwargs["bike_id"])
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["bike_id"] = self.kwargs["bike_id"]
        return context_data
    
    def test_func(self):
        selected_bike = Bike.objects.get(pk=self.kwargs["bike_id"])
        if super().test_func() and self.request.user == selected_bike.owner:
            return True
        else:
            return False    


class FastServiceOrderReservationView(RegularUserRequiredSuccessMessageMixin, FormView):
    model = FastServiceOrder
    form_class = FastServiceOrderReservationForm
    template_name = 'core/fast_service_order_reserve_form.html'
    success_message = _("Naročilo uspešno rezervirano.")
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        month, year = get_current_month_and_year()
        calendar_data = create_calendar_data(month, year, True)
        context_data["month"] = month
        context_data["year"] = year
        context_data["calendar_data"] = calendar_data
        return context_data
    
    def get_success_url(self) -> str:
        return reverse('core:bike_history', kwargs=self.kwargs)
    
    def form_valid(self, form):
        user = self.request.user
        bike = Bike.objects.get(pk=self.kwargs["bike_id"])
        form.save(user, bike)
        form.cleaned_data["online_appointment"].delete()
        return super().form_valid(form)


class FastServiceOrderDetailsView(RegularUserRequiredMixin, DetailView):
    model = FastServiceOrder
    pk_url_kwarg = "service_order_id"
    template_name = "core/service_order_details.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["full_bike_title"] = self.object.bike
        context_data["first_name"] = self.object.user.first_name
        context_data["last_name"] = self.object.user.last_name
        context_data["email"] = self.object.user.email
        context_data["phone_number"] = self.object.user.profile.phone_number
        context_data["address"] = self.object.user.profile.address
        context_data["user"] = self.request.user
        context_data["service_order_type"] = "fast"
        context_data["comments"] = FastServiceOrderStaffComment.objects.filter(
            service_order_id=self.kwargs[self.pk_url_kwarg])
        return context_data
    
    def test_func(self) -> bool | None:
        if self.get_object().user == self.request.user or self.request.user.is_staff:
                return True
        return False


class ManualServiceOrderDetailsView(StaffRequiredSuccessMessageMixin, DetailView):
    model = ManualServiceOrder
    pk_url_kwarg = "service_order_id"
    template_name = "core/service_order_details.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["full_bike_title"] = self.object.full_bike_title
        context_data["first_name"] = self.object.first_name
        context_data["last_name"] = self.object.last_name
        context_data["email"] = self.object.email
        context_data["phone_number"] = self.object.phone_number
        context_data["address"] = self.object.address
        context_data["user"] = self.request.user
        context_data["service_order_type"] = "manual"
        context_data["comments"] = ManualServiceOrderStaffComment.objects.filter(
            service_order_id=self.kwargs[self.pk_url_kwarg])
        return context_data