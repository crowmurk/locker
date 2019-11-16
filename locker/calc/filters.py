from django.db.models import Q
from django.http.request import QueryDict
from django.utils.translation import gettext_lazy as _

from django_filters import (
    FilterSet,
    CharFilter,
    NumberFilter,
    DateFilter,
)

from .models import Order, Service, OrderOption
from django.forms import DateInput


class OrderFilter(FilterSet):
    id = NumberFilter(label=_('Estimate'))
    author = CharFilter(method='author_filter')
    client = CharFilter(method='client_filter')
    created__gte = DateFilter(
        label=_('Created from'),
        field_name='created',
        lookup_expr='gte',
        widget=DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    created__lte = DateFilter(
        label=_('Created to'),
        field_name='created',
        lookup_expr='lte',
        widget=DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )

    class Meta:
        model = Order
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        user = getattr(kwargs.get('request'), 'user', None)
        if user and not user.is_superuser:
            if data is None:
                data = QueryDict()
            data = data.copy()
            data['author'] = user.get_full_name()

        super(OrderFilter, self).__init__(data, *args, **kwargs)

    def author_filter(self, queryset, name, value):
        for word in value.split():
            queryset = queryset.filter(
                Q(author__first_name__icontains=word) | Q(author__last_name__icontains=word)
            )
        return queryset

    def client_filter(self, queryset, name, value):
        return queryset.filter(
            Q(client__name__icontains=value) |
            Q(branch__name__icontains=value) |
            Q(branch__settlement__icontains=value) |
            Q(branch__address__icontains=value)
        )


class ServiceFilter(FilterSet):
    equipment = CharFilter(method='equipment_filter')
    rating__gte = NumberFilter(
        label=_('Rating from'),
        field_name='rating',
        lookup_expr='gte',
    )
    rating__lte = NumberFilter(
        label=_('Rating to'),
        field_name='rating',
        lookup_expr='lte',
    )

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
        label=_('Equipment'),
        field_name='service__equipment',
        lookup_expr='icontains',
    )

    class Meta:
        model = OrderOption
        fields = []
