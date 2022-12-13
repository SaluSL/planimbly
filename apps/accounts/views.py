from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from rest_framework import viewsets

from apps.accounts.models import Employee
from apps.accounts.serializers import EmployeeSerializer
from apps.organizations.views import send_user_activation_mail
from planimbly.permissions import Issupervisor, GroupRequiredMixin


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [Issupervisor]

    def get_queryset(self):
        queryset = Employee.objects.all().filter(user_org=self.request.user.user_org) \
            .exclude(is_supervisor=True)
        return queryset

    def perform_create(self, serializer):
        v_data = serializer.validated_data
        password = Employee.objects.make_random_password()
        employee = get_user_model().objects.create_user(email=v_data.get('email'), username=v_data.get('username'),
                                                        first_name=v_data.get('first_name'),
                                                        last_name=v_data.get('last_name'),
                                                        order_number=v_data.get('order_number'), password=password,
                                                        job_time=v_data.get('job_time'),
                                                        user_org=self.request.user.user_org)
        send_user_activation_mail(employee, self.request)


class EmployeeOptionView(GroupRequiredMixin, TemplateView):
    template_name = 'accounts/employee_option.html'
