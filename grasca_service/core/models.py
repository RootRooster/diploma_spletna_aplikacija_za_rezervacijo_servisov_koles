from datetime import date
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class FreeOnlineAppointment(models.Model):
    date = models.DateField()
    vip_reserved = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(date__week_day=1),
                name='%(app_label)s_%(class)s_date_not_sunday'
            )
        ]
    
    def __str__(self) -> str:
        return self.date.strftime("%d-%m-%Y")
    
    @property
    def event_color(self) -> str:
        if self.vip_reserved:
            return "gold"
        return "green"
    
    def get_update_url(self) -> str:
        return reverse("core:edit_free_online_appoitment", kwargs={"service_order_id": self.pk})


class Bike(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.brand} {self.model} {self.year}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class ServiceOrder(models.Model):
    SERVICE_CHOICES = {
        "blue": _("Prvi servis"),
        "orange": _("Mali servis"),
        "red": _("Veliki servis")
    }
    SERVICE_STATUS_CHOICES = {
        0: _("Nedostavljen"),
        1: _("Dostavljen"),
        2: _("V delu"),
        3: _("Končan"),
        4: _("Prevzet")
    }
    date = models.DateField()
    service_type = models.CharField(max_length=6, choices=SERVICE_CHOICES)
    status = models.PositiveSmallIntegerField(choices=SERVICE_STATUS_CHOICES, default=0)
    service_number = models.PositiveIntegerField(null=True, blank=True)
    assigned_staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_assigned_staff")
    comment = models.TextField(null=True, blank=True)

    @property
    def event_status_urgency(self) -> str:
        if self.status == 0 and self.date == date.today():
            return "text-bg-danger"
        elif self.status == 1:
            return "text-bg-info"
        elif self.status == 2:
            return "text-bg-warning"
        elif self.status == 3:
            return "text-bg-success"
        elif self.status == 4:
            return "text-bg-dark"
        else:
            return ""
    
    @property
    def event_color(self) -> str:
        if self.status == 3 or self.status == 4:
            return "gray"
        else:
            return self.service_type
    
    class Meta:
        abstract = True
        
        constraints = [
            models.CheckConstraint(
                check=~Q(date__week_day=1),
                name='%(app_label)s_%(class)s_date_not_sunday'
            )
        ]


class ManualServiceOrder(ServiceOrder):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100)
    full_bike_title = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    
    def get_update_url(self) -> str:
        return reverse("core:edit_manual_service_order", kwargs={"service_order_id": self.pk})
    
    def get_details_url(self) -> str:
        return reverse("core:manual_service_order_details", kwargs={"service_order_id": self.pk})
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class FastServiceOrder(ServiceOrder):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    
    def get_update_url(self) -> str:
        return reverse("core:edit_fast_service_order", kwargs={"service_order_id": self.pk})
    
    def get_details_url(self) -> str:
        return reverse("core:fast_service_order_details", kwargs={"service_order_id": self.pk})
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class ServiceOrderStaffComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} - {self.date_time.strftime('%d-%m-%Y')}"
    
    class Meta:
        abstract = True


class ManualServiceOrderStaffComment(ServiceOrderStaffComment):
    service_order = models.ForeignKey(ManualServiceOrder, on_delete=models.CASCADE, related_name="comments")
    

class FastServiceOrderStaffComment(ServiceOrderStaffComment):
    service_order = models.ForeignKey(FastServiceOrder, on_delete=models.CASCADE, related_name="comments")
    
    
    


    