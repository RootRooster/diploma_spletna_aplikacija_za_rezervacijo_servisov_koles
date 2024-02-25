from datetime import datetime, date
from django.utils import timezone
from django.utils.translation import gettext as _
import calendar

from core.models import FastServiceOrder, FreeOnlineAppointment, ManualServiceOrder


def get_current_month_and_year():
    """Return current month and year as tuple.

    Returns:
        tuple: (int, int)
    """
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year
    return current_month, current_year


def get_num_of_days(year, month):
    """Return ammount of days in a given month.

    Args:
        year (int): The year.
        month (int): The month.

    Returns:
        int: Ammount of days in a given month.
    """
    _, num_of_days = calendar.monthrange(year, month)
    return num_of_days


def get_slovenian_month_name(month):
    """Return slovenian month name.

    Args:
        month (int): The month.

    Returns:
        str: Slovenian month name.
    """
    slovenian_month_names = {
        1: _("Januar"),
        2: _("Februar"),
        3: _("Marec"),
        4: _("April"),
        5: _("Maj"),
        6: _("Junij"),
        7: _("Julij"),
        8: _("Avgust"),
        9: _("September"),
        10: _("Oktober"),
        11: _("November"),
        12: _("December")
    }
    return slovenian_month_names[month]


def get_appointments_and_service_orders(day, year, month):
    """Return appointments and service orders for a given day.
    
    Args:
        day (int): The day.
        year (int): The year.
        month (int): The month.
        
    Returns:
        dict: Appointments and service orders for a given day. It also returns the day itself and a boolean that tells if the day is today.
    """
    return {
        "day": day,
        "is_today": day == timezone.now().day and month == timezone.now().month and year == timezone.now().year,
        "events": [
            FreeOnlineAppointment.objects.filter(date=date(year, month, day)),
            FastServiceOrder.objects.filter(date=date(year, month, day)),
            ManualServiceOrder.objects.filter(date=date(year, month, day))   
        ]
    }


def create_calendar_data(month, year):
    """Return calendar data for a given month and year.
    
    Args:
        month (int): The month.
        year (int): The year.
        
    Returns:
        dict: calendar data for a given month and year. Calendar data consists of:
            - month (tuple): Slovenian month name and month number.
            - year (int): The year.
            - weeks (list): List of weeks. Each week is a list of days. Each day is a dict that contains appointments and service orders for that day.
    """
    calendar_data = {}
    calendar_data["month"] = (get_slovenian_month_name(month), month)
    calendar_data["year"] = year
    calendar_data_week = []
    num_of_days = get_num_of_days(year, month)
    day = 1
    curr_date = datetime(year, month, day)
    weekday = curr_date.weekday()
    calendar_data_days = []
    for i in range(0, weekday):
        calendar_data_days.append(None)
    while(day <= num_of_days):
        if len(calendar_data_days) > 6:
            calendar_data_week.append(calendar_data_days)
            calendar_data_days = []
        calendar_data_days.append(get_appointments_and_service_orders(day, year, month))
        day += 1
    while(len(calendar_data_days) < 7):
        calendar_data_days.append(None)
    calendar_data_week.append(calendar_data_days)
    calendar_data["weeks"] = calendar_data_week
    return calendar_data