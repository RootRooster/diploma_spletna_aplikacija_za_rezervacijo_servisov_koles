from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff and not self.request.user.is_superuser and self.request.user.is_authenticated


class RegularUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_staff and self.request.user.is_authenticated and not self.request.user.is_superuser


class RegularUserRequiredSuccessMessageMixin(RegularUserRequiredMixin, SuccessMessageMixin):
    pass


class StaffRequiredSuccessMessageMixin(StaffRequiredMixin, SuccessMessageMixin):
    pass

