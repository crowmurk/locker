from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from core.tables import CheckBoxActionColumn

from .models import Order, Service, OrderOption


class OrderTable(tables.Table):
    id = tables.LinkColumn(verbose_name=_('Order'))
    author = tables.Column(
        accessor='author.get_full_name',
        order_by=('author.first_name', 'author.last_name', ),
    )
    branch = tables.LinkColumn(text=lambda record: record.branch.name)
    address = tables.Column(
        accessor='branch.address',
        verbose_name=_('Address'),
    )
    client = tables.LinkColumn()
    price = tables.Column(verbose_name=_("Price"))
    delete = CheckBoxActionColumn(
        accessor="pk",
        script={'button_name': 'action-table-button', },
    )

    class Meta:
        model = Order
        sequence = (
            'id',
            'author',
            'client',
            'branch',
            'address',
            'created',
            'modified',
            'price',
        )
        exclude = ('factor', )
        empty_text = _("There are no records available")


class OrderCreateServiceTable(tables.Table):
    equipment = tables.LinkColumn()
    price = tables.Column(verbose_name=_("Total"))
    add = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Service
        sequence = (
            'rating',
            'equipment',
            'work',
            'price',
        )
        exclude = (
            'id',
            'equipment_price',
            'work_price',
        )
        empty_text = _("There are no records available")


class ServiceTable(tables.Table):
    price = tables.Column(verbose_name=_("Total"))
    equipment = tables.LinkColumn()
    delete = CheckBoxActionColumn(
        accessor="pk",
        script={'button_name': 'action-table-button', },
    )

    class Meta:
        model = Service
        sequence = (
            'rating',
            'equipment',
            'equipment_price',
            'work',
            'work_price',
            'price',
        )
        exclude = ('id', )
        empty_text = _("There are no records available")


class OrderOptionTable(tables.Table):
    order = tables.LinkColumn(text=lambda record: record.order.pk)
    service = tables.LinkColumn(text=lambda record: record.service.equipment)
    service_price = tables.Column(
        accessor='service.price',
        verbose_name=_('Price')
    )
    price = tables.Column(verbose_name=_("Sum"))
    delete = CheckBoxActionColumn(
        accessor="pk",
        script={'button_name': 'action-table-button', },
    )

    class Meta:
        model = OrderOption
        sequence = ('order', 'service', 'service_price', 'quantity', 'price')
        exclude = ('id', )
        empty_text = _("There are no records available")
