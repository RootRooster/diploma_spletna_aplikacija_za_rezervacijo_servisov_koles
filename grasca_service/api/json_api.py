from django.http import HttpResponseForbidden, JsonResponse
from core.models import Bike
from django.contrib.auth.decorators import login_required

@login_required
def get_bikes_of_user(request):
    """Get all bikes of a user.
    The requests data should contain the following parameters:
        - user_id: int
    
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()
    bikes = Bike.objects.filter(owner_id=request.GET.get('user'))
    return JsonResponse({"bikes": list(bikes.values())})
    