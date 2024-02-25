from django.shortcuts import render

from .helpers import create_calendar_data, get_current_month_and_year

# big calander is meant for the employee dashboard
def get_next_month_big(request):
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    month += 1
    if month > 12:
        month = 1
        year += 1
    calendar_data = create_calendar_data(month, year)
    return render(request, "_calendar_big.html", locals())

def get_previous_month_big(request):
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    month -= 1
    if month < 1:
        month = 12
        year -= 1
    calendar_data = create_calendar_data(month, year)
    return render(request, "_calendar_big.html", locals())

def get_current_month_big(request):
    month, year = get_current_month_and_year()
    calendar_data = create_calendar_data(month, year)
    return render(request, "_calendar_big.html", locals())

def get_next_month_small(request):
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    month += 1
    if month > 12:
        month = 1
        year += 1
    calendar_data = create_calendar_data(month, year)
    return render(request, "_calendar_small.html", locals())

def get_previous_month_small(request):
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    month -= 1
    if month < 1:
        month = 12
        year -= 1
    calendar_data = create_calendar_data(month, year)
    return render(request, "_calendar_small.html", locals())

def get_current_month_small(request):
    month, year = get_current_month_and_year()
    calendar_data = create_calendar_data(month, year)
    return render(request, "_calendar_small.html", locals())
