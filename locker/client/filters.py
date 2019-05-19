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
    number_of_orders = RangeFilter(
        label=_('Orders'),
    )

    class Meta:
        model = Client
        fields = []

    def client_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(details__icontains=value)
        )


class BranchFilter(FilterSet):
    branch = CharFilter(
        label=_('Branch'),
        method='branch_filter',
    )
    client = CharFilter(
        label=_('Client'),
        field_name='client__name',
        lookup_expr='icontains',
    )
    number_of_orders = RangeFilter(
        label=_('Orders'),
    )

    class Meta:
        model = Branch
        fields = []

    def branch_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(address__icontains=value)
        )
