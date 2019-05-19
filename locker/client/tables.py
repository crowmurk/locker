from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from core.tables import CheckBoxActionColumn

from .models import Client, Branch


class ClientTable(tables.Table):
    name = tables.LinkColumn()
    number_of_branches = tables.Column(
        verbose_name=_("Number of branches"),
    )
    number_of_orders = tables.Column(
        verbose_name=_("Number of orders"),
    )
    delete = CheckBoxActionColumn(
        accessor="pk",
        script={'button_name': 'action-table-button', },
    )

    class Meta:
        model = Client
        exclude = ('id', 'slug')
        empty_text = _("There are no records available")


class BranchTable(tables.Table):
    name = tables.LinkColumn()
    client = tables.LinkColumn(
        text=lambda record: record.client.name,
    )
    number_of_orders = tables.Column(
        verbose_name=_("Number of orders"),
    )
    delete = CheckBoxActionColumn(
        accessor="pk",
        script={'button_name': 'branch-table-button',
                'header_name': 'branch-table-column-header',
                'selection_name': 'branch-table-column-item',
                },
    )

    class Meta:
        model = Branch
        sequence = (
            'name',
            'address',
            'client',
            'number_of_orders',
        )
        exclude = ('id', )
        empty_text = _("There are no records available")
