from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2.utils import A

from .models import Order, Service, OrderOption


class OrderTable(tables.Table):
    id = tables.LinkColumn()
    author = tables.Column(accessor='author.get_full_name')
    client = tables.LinkColumn()
    price = tables.Column(
        verbose_name=_("Price"),
    )

    class Meta:
        model = Order


class ServiceTable(tables.Table):
    price = tables.Column(
        verbose_name=_("Total"),
    )
    equipment = tables.LinkColumn()

    class Meta:
        model = Service
        exclude = ('id', )


class OrderOptionTable(tables.Table):
    service = tables.LinkColumn(
        'calc:service:detail',
        text=lambda record: record.service.equipment,
        args=[A('service.pk')],
    )
    service_price = tables.Column(
        accessor='service.price',
        verbose_name=_('Price')
    )
    price = tables.Column(
        verbose_name=_("Sum"),
    )

    class Meta:
        model = OrderOption
        sequence = ('id', 'service', 'service_price', 'quantity', 'price')
        exclude = ('id', 'order')
