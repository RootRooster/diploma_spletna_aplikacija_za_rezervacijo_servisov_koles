from datetime import date
from django.contrib.auth.models import User
from core.models import FastServiceOrder, ManualServiceOrder


def get_service_orders_for_user(user: User, src_date: date = date.today()):
    my_tasks_manual = ManualServiceOrder.objects.filter(date=src_date, assigned_staff=user)
    my_tasks_fast = FastServiceOrder.objects.filter(date=src_date, assigned_staff=user)
    return my_tasks_manual, my_tasks_fast