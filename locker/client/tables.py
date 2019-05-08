from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from core.tables import CheckBoxActionColumn

from .models import Client


class ClientTable(tables.Table):
    name = tables.LinkColumn()
    number_of_orders = tables.Column(
        verbose_name=_("Number of orders"),
    )
    delete = CheckBoxActionColumn(
        accessor="pk",
        script={'button_name': 'action-table-delete-button', },
    )

    class Meta:
        model = Client
        exclude = ('id', 'slug')
        empty_text = _("There are no records available")
