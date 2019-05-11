from django.db.models import Count
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django_filters import (
    FilterSet,
    CharFilter,
    RangeFilter,
)

from .models import Client, Branch


class ClientFilter(FilterSet):
    client = CharFilter(
        label=_('Client'),
        method='client_filter',
    )

    orders = RangeFilter(
        label=_('Orders'),
        method='number_of_orders_filter',
    )

    class Meta:
        model = Client
        fields = []

    def client_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(details__icontains=value)
        )

    def number_of_orders_filter(self, queryset, name, value):
        if value:
            if value.start is not None and value.stop is not None:
                lookup_expr = 'range'
                value = (value.start, value.stop)
            elif value.start is not None:
                lookup_expr = 'gte'
                value = value.start
            elif value.stop is not None:
                lookup_expr = 'lte'
                value = value.stop

            annotate_field = 'orders_number'
            queryset = Client.objects.annotate(
                **{annotate_field: Count('orders')},
            )
            queryset = queryset.filter(
                **{'__'.join([annotate_field, lookup_expr]): value},
            )

        return queryset


class BranchFilter(FilterSet):
    client = CharFilter(
        label=_('Client'),
        field_name='client__name',
        lookup_expr='icontains',
    )
    branch = CharFilter(
        label=_('Branch'),
        method='branch_filter')

    class Meta:
        model = Branch
        fields = []

    def branch_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(address__icontains=value)
        )
