import django_filters

from .models import Order, Service, OrderOption


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = {
            'author__last_name': ['icontains', ],
        }


class ServiceFilter(django_filters.FilterSet):

    class Meta:
        model = Service
        fields = {
            'equipment': ['icontains', ],
        }


class OrderOptionFilter(django_filters.FilterSet):

    class Meta:
        model = OrderOption
        fields = {
            'service__equipment': ['icontains', ],
        }
