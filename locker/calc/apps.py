from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CalcConfig(AppConfig):
    name = 'calc'
    verbose_name = _('Calculator')
