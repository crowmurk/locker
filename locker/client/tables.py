from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from core.tables import CheckBoxDeleteColumn

from .models import Client


class ClientTable(tables.Table):
    name = tables.LinkColumn()
    number_of_orders = tables.Column(
        verbose_name=_("Number of orders"),
    )
    delete = CheckBoxDeleteColumn(accessor="pk")

    class Meta:
        model = Client
        exclude = ('id', 'slug')
        empty_text = _("There are no records available")
