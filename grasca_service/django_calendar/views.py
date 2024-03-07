from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .helpers import create_calendar_data, get_current_month_and_year
from django.http import HttpResponseForbidden
# big calander is meant for the employee dashboard
@login_required
def get_next_month_big(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    month += 1
    if month > 12:
        month = 1
        year += 1
    calendar_data = create_calendar_data(month, year, True)
    return render(request, "_calendar_big.html", locals())

@login_required
def get_previous_month_big(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    month -= 1
    if month < 1:
        month = 12
        year -= 1
    calendar_data = create_calendar_data(month, year, True)
    return render(request, "_calendar_big.html", locals())

@login_required
def get_current_month_big(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    month, year = get_current_month_and_year()
    calendar_data = create_calendar_data(month, year, True)
    return render(request, "_calendar_big.html", locals())


def get_next_month_small(request):
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    month += 1
    if month > 12:
        month = 1
        year += 1
    if request.user.is_authenticated:
        calendar_data = create_calendar_data(month, year, True)
    else:
        calendar_data = create_calendar_data(month, year, False)
    return render(request, "_calendar_small.html", locals())


def get_previous_month_small(request):
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    month -= 1
    if month < 1:
        month = 12
        year -= 1
    if request.user.is_authenticated:
        calendar_data = create_calendar_data(month, year, True)
    else:
        calendar_data = create_calendar_data(month, year, False)
    return render(request, "_calendar_small.html", locals())


def get_current_month_small(request):
    month, year = get_current_month_and_year()
    if request.user.is_authenticated:
        calendar_data = create_calendar_data(month, year, True)
    else:
        calendar_data = create_calendar_data(month, year, False)
    return render(request, "_calendar_small.html", locals())


