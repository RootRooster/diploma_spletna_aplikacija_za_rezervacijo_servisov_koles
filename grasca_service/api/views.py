from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from datetime import date
from django.contrib.auth.decorators import login_required
from core.models import FreeOnlineAppointment, ManualServiceOrderStaffComment, FastServiceOrderStaffComment
from django_calendar.helpers import create_calendar_data
from datetime import datetime

from core.helpers import get_service_orders_for_user

@login_required
def create_new_free_appointment(request):
    """This view is used to create a new free appointment. 
    The request should contain the following parameters:
    - day: str (1-31)
    - month: str (1-12)
    - year: str (2021-...)
    - vip: str (0 or 1)
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()
    day = int(request.GET.get('day'))
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    vip = True if int(request.GET.get('vip')) == 1 else False
    date_object = date(year, month, day)
    FreeOnlineAppointment.objects.create(date=date_object, vip_reserved=vip)
    calendar_data = create_calendar_data(month, year, True)
    return render(request, "_calendar_big.html", locals())

@login_required
def get_personal_daily_calander(request):
    """This view is used to get the personal daily calendar for the current user. 
    The request should contain the following get parameters:
    - my-cal-selected-date: str (2021-01-01)
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()
    selected_date = request.GET.get('my-cal-selected-date')
    src_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    my_tasks_manual, my_tasks_fast = get_service_orders_for_user(request.user, src_date)
    return render(request, "components/_service_order_daily_cards.html", locals())


@login_required
def post_comments_and_return_staff_comments(request):
    """This view is used to post comments and return the staff comments for the current user. 
    The request should contain the following get parameters:
    - service_order_id: str (1-...)
    - comment: str
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()
    try:
        service_order_type = request.POST.get("service_order_type")
        service_order_id = request.POST.get("service_order_id")
        new_comment = request.POST.get("new_comment")
        comments = None
        if request.POST.get("service_order_type") == "manual":
            ManualServiceOrderStaffComment.objects.create(
                service_order_id=service_order_id,
                user=request.user,
                comment=new_comment
            )
            comments = ManualServiceOrderStaffComment.objects.filter(service_order_id=service_order_id)
        elif request.POST.get("service_order_type") == "fast":
            FastServiceOrderStaffComment.objects.create(
                service_order_id=service_order_id,
                user=request.user,
                comment=new_comment
            )
            comments = FastServiceOrderStaffComment.objects.filter(service_order_id=service_order_id)
        return render(request, "components/_staff_comments.html", locals())
    except:
        return HttpResponseBadRequest()
    
