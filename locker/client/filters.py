import django_filters

from .models import Client, Branch


class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = {
            'name': ['icontains', ],
        }


class BranchFilter(django_filters.FilterSet):
    class Meta:
        model = Branch
        fields = {
            'name': ['icontains', ],
        }
