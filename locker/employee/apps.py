from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmployeeConfig(AppConfig):
    name = 'employee'
    verbose_name = _('Employees')

    def ready(self):
        import employee.signals
