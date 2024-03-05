from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages

from django_calendar.helpers import create_calendar_data, get_current_month_and_year
from core.models import ManualServiceOrder
from core.helpers import get_service_orders_for_user

from .forms import QuickServiceForm


def home_page_view(request):
    instructions = [
        {
            "heading": _("1. Naroči Se Na Termin"),
            "text": _("Izpolni obrazec s svojimi podatki in izberi želeni tip servisa. Preveri razpoložljive termine na koledarju ali se registriraj na naši spletni strani."),
            "icon": "fas fa-calendar-check"
        },
        {
            "heading": _("2. Kolo Pripelji Na Servis"),
            "text": _("Prinesi kolo na servis dan pred dogovorjenim terminom ali istega dne zjutraj."),
            "icon": "fas fa-bicycle"
        },
        {
            "heading": _("3. Čas, Ko Je Kolo Na Servisu"),
            "text": _("V času servisa imej telefon pri sebi za morebitne klice ali SMS-e v zvezi s servisom."),
            "icon": "fas fa-clock"
        },
        {
            "heading": _("4. Prejetje SMSa"),
            "text": _("Ko prejmeš SMS o zaključenem servisu, lahko prevzameš kolo."),
            "icon": "fas fa-sms"
        }
    ]
    faq_data = [
        {
            "question": _("Kako dolgo traja servis?"),
            "answer": _("Servis traja od 1 do 3 dni, odvisno od obsega dela.")
        },
        {
            "question": _("Kakšne so cene servisov?"),
            "answer": _("Cene servisov so odvisne od vrste servisa in obsega dela. Prvi servis je brezplačen. Mali servis in veliki servis sta odvisna od količine dela in potrebnih rezervnih delov. Približno pa se cena malega servisa giblje med 30 in 50 evrov, cena velikega servisa pa med 100-150 evrov. Natančno ceno servisa ti sporočimo po pregledu kolesa oziroma sproti, če se med servisom najde dodatna dela.")
        },
        {
            "question": _("Kaj potrebujem imeti sabo na dan servisa?"),
            "answer": _("Na dan servisa potrebujete le kolo in osebni dokument. Vse ostalo poskrbimo mi."),
        },
        {
            "question": _("Kako izberem pravo vrsto servisa?"),
            "answer": _("Izberi vrsto servisa glede na to, kaj potrebuje tvoje kolo. Če kolo še ni bilo na servisu, je novo in kupljeno pri nas, izberi prvi servis. Če je na kolesu potrebna menjava vzmetnice, nastavitev menjalnika ali zavor, izberi mali servis. Če je potrebno kolo popolnoma razstaviti, očistiti in zamenjati vse obrabljene dele, izberi veliki servis.")
        }
    ]
    month, year = get_current_month_and_year()
    calendar_data = create_calendar_data(month, year)
    form = QuickServiceForm()
    if request.method == "POST":
        form = QuickServiceForm(request.POST)
        if form.is_valid():
            ManualServiceOrder.objects.create(
                date=form.cleaned_data["online_appointment"].date,
                service_type=form.cleaned_data["service_type"],
                full_bike_title=form.cleaned_data["full_bike_title"],
                address=form.cleaned_data["address"],
                phone_number=form.cleaned_data["phone_number"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                comment=form.cleaned_data["comment"]
            )
            form.cleaned_data["online_appointment"].delete()
            messages.success(request, _("Naročilo uspešno ustvarjeno."))
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect(reverse("home:staff_home_page"))
        else:
            return redirect(reverse("home:profile_home_page"))
    return render(request, "home/home_page.html", locals())


@login_required
def staff_home_page_view(request):
    if not request.user.is_staff:
        return redirect(reverse("home:profile_home_page"))
    month, year = get_current_month_and_year()
    calendar_data = create_calendar_data(month, year)
    my_tasks_manual, my_tasks_fast = get_service_orders_for_user(request.user)
    return render(request, "home/staff_home_page.html", locals())


@login_required
def profile_home_page_view(request):
    if request.user.is_staff:
        return redirect(reverse("home:staff_home_page"))
    month, year = get_current_month_and_year()
    calendar_data = create_calendar_data(month, year)
    bikes = request.user.bike_set.all()
    return render(request, "home/profile_home_page.html", locals())
