from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from core.views import DeleteColumnMixin
from calc.tables import OrderTable
from calc.models import Order

from .models import Client
from .tables import ClientTable
from .forms import ClientForm
from .filters import ClientFilter


class ClientList(SingleTableMixin, DeleteColumnMixin, FilterView):
    model = Client
    table_class = ClientTable
    filterset_class = ClientFilter
    template_name = 'client/client_list.html'


class ClientCreate(CreateView):
    model = Client
    form_class = ClientForm


class ClientDetail(DetailView, DeleteColumnMixin):
    model = Client
    related_model = Order
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(object=self.object)
        context['table'] = OrderTable(self.object.get_orders(), exclude=('client', ))
        return context


class ClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm


class ClientDelete(DeleteView):
    model = Client
    success_url = reverse_lazy('client:list')
