import datetime

from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .models import Order, Service, OrderOption


class DurationColumnMixin:
    def render_work_duration(self, value):
        if isinstance(value, datetime.timedelta):
            seconds = int(value.total_seconds())
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            return '{:d}:{:02d}'.format(hours, minutes)

        return value


class OrderTable(DurationColumnMixin, tables.Table):
    id = tables.LinkColumn(verbose_name=_('Estimate'))
    author = tables.Column(
        accessor='author.get_full_name',
        order_by=('author.first_name', 'author.last_name', ),
    )
    client = tables.Column(
        linkify=(
            'client:detail',
            {'slug': tables.A('client.slug'), },
        ),
        accessor='client.name',
        verbose_name=_('Client'),
    )
    branch = tables.Column(
        linkify=(
            'client:branch:detail',
            {
                'client_slug': tables.A('client.slug'),
                'pk': tables.A('branch.pk'),
            },
        ),
        accessor='branch.name',
        verbose_name=_('Branch'),
    )
    address = tables.Column(
        accessor='branch.address',
        verbose_name=_('Address'),
    )
    price = tables.Column(verbose_name=_("Total price"))
    delete = tables.CheckBoxColumn(accessor="pk")

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
        exclude = ('settlement', 'factor', )
        empty_text = _("There are no records available")

    def render_address(self, record, value):
        return "{settlement}, {address}".format(
            settlement=record.branch.settlement,
            address=value,
        )


class OrderCreateServiceTable(tables.Table):
    equipment = tables.LinkColumn()
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
            'work_duration',
        )
        empty_text = _("There are no records available")


class ServiceTable(DurationColumnMixin, tables.Table):
    equipment = tables.LinkColumn()
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Service
        sequence = (
            'rating',
            'equipment',
            'equipment_price',
            'work',
            'work_price',
            'work_duration',
            'price',
        )
        exclude = ('id', )
        empty_text = _("There are no records available")


class OrderOptionTable(DurationColumnMixin, tables.Table):
    order = tables.Column(
        linkify=(
            'calc:order:detail',
            {'pk': tables.A('order.pk'), },
        ),
        accessor='order.pk',
        verbose_name=_('Estimate'),
    )
    service = tables.Column(
        linkify=(
            'calc:service:detail',
            {'pk': tables.A('service.pk'), },
        ),
        accessor='service.equipment',
        verbose_name=_('Equipment'),
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = OrderOption
        sequence = (
            'order',
            'service',
            'equipment_price',
            'work_price',
            'quantity',
            'price',
        )
        exclude = ('id', )
        empty_text = _("There are no records available")
