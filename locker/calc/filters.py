from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django_filters import (
    FilterSet,
    CharFilter,
    DateFromToRangeFilter,
    NumberFilter,
    RangeFilter,
)
from django_filters.widgets import RangeWidget

from .models import Order, Service, OrderOption


class OrderFilter(FilterSet):
    author = CharFilter(method='author_filter')
    client = CharFilter(method='client_filter')
    created = DateFromToRangeFilter(
        widget=RangeWidget(
            attrs={'placeholder': _('DD.MM.YYYY')},
        ),
    )

    class Meta:
        model = Order
        fields = []

    def author_filter(self, queryset, name, value):
        for word in value.split():
            queryset = queryset.filter(
                Q(author__first_name__icontains=word) | Q(author__last_name__icontains=word)
            )
        return queryset

    def client_filter(self, queryset, name, value):
        return queryset.filter(
            Q(client__name__icontains=value) | Q(branch__name__icontains=value) | Q(branch__address__icontains=value)
        )


class ServiceFilter(FilterSet):
    equipment = CharFilter(method='equipment_filter')
    rating = RangeFilter()

    class Meta:
        model = Service
        fields = []

    def equipment_filter(self, queryset, name, value):
        return queryset.filter(
            Q(equipment__icontains=value) | Q(work__icontains=value)
        )


class OrderOptionFilter(FilterSet):
    order = NumberFilter()
    equipment = CharFilter(
        label=_('Service'),
        field_name='service__equipment',
        lookup_expr='icontains',
    )

    class Meta:
        model = OrderOption
        fields = []
