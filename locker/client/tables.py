from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .models import Client, Branch


class ClientTable(tables.Table):
    name = tables.LinkColumn()
    number_of_branches = tables.Column(
        verbose_name=_("Number of branches"),
    )
    number_of_orders = tables.Column(
        verbose_name=_("Number of orders"),
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Client
        exclude = ('id', 'slug')
        empty_text = _("There are no records available")


class BranchTable(tables.Table):
    name = tables.LinkColumn()
    client = tables.Column(
        linkify=(
            'client:detail',
            {'slug': tables.A('client.slug'), },
        ),
        accessor='client.name',
        verbose_name=_("Client"),
    )
    number_of_orders = tables.Column(
        verbose_name=_("Number of orders"),
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Branch
        sequence = (
            'name',
            'settlement',
            'address',
            'client',
            'number_of_orders',
        )
        exclude = ('id', )
        empty_text = _("There are no records available")
