from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableView, SingleTableMixin, MultiTableMixin
from django_filters.views import FilterView

from core.views import ActionTableDeleteMixin
from calc.tables import OrderTable
from calc.models import Order

from .models import Client, Branch
from .tables import ClientTable, BranchTable
from .forms import ClientForm, BranchForm
from .filters import ClientFilter, BranchFilter
from .utils import ClientContextMixin, BranchGetObjectMixin


class ClientList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Client
    action_table_model = Client
    table_class = ClientTable
    filterset_class = ClientFilter
    template_name = 'client/client_list.html'


class ClientCreate(CreateView):
    model = Client
    form_class = ClientForm


class ClientDetail(MultiTableMixin, ActionTableDeleteMixin, DetailView):
    model = Client
    form_class = ClientForm
    action_table_multitables = {
        'action-table-button': Order,
        'branch-table-button': Branch,
    }

    def get_tables(self):
        self.tables = [
            OrderTable(self.object.get_orders(), exclude=('client', )),
            BranchTable(self.object.get_branches(), exclude=('client', )),
        ]
        tables = super(ClientDetail, self).get_tables()
        return tables


class ClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm


class ClientDelete(DeleteView):
    model = Client
    success_url = reverse_lazy('client:list')


class BranchList(
        SingleTableMixin,
        ActionTableDeleteMixin,
        FilterView,
):
    model = Branch
    action_table_model = Branch
    action_table_button = 'branch-table-button'
    table_class = BranchTable
    filterset_class = BranchFilter
    template_name = 'client/branch_list.html'


class BranchListClient(
        BranchGetObjectMixin,
        ClientContextMixin,
        SingleTableView,
        ActionTableDeleteMixin,
):
    model = Branch
    action_table_model = Branch
    action_table_button = 'branch-table-button'
    table_class = BranchTable
    template_name = 'client/branch_list.html'

    def get_table_data(self):
        client_slug = self.kwargs.get(self.client_slug_url_kwarg)
        client = Client.objects.get(slug__iexact=client_slug)
        return client.get_branches()


class BranchCreate(BranchGetObjectMixin, ClientContextMixin, CreateView):
    model = Branch
    form_class = BranchForm

    def get_initial(self):
        """Добавляет ассоциированный с branch client
        в контекст представления
        """
        # Получаем ассоциированный client
        client_slug = self.kwargs.get(self.client_slug_url_kwarg)
        self.client = get_object_or_404(Client, slug__iexact=client_slug)
        # Добавляем к начальным данным представления
        initial = {self.client_context_object_name: self.client, }
        initial.update(self.initial)
        return initial


class BranchDetail(
        BranchGetObjectMixin,
        ClientContextMixin,
        SingleTableMixin,
        ActionTableDeleteMixin,
        DetailView,
):
    model = Branch
    form_class = BranchForm
    action_table_model = Order
    table_class = OrderTable

    def get_table_kwargs(self):
        return {
            'exclude': ('client', 'branch', 'address', )
        }

    def get_table_data(self):
        client_slug = self.kwargs.get(self.client_slug_url_kwarg)
        return Order.objects.filter(
            client__slug__iexact=client_slug,
            branch=self.object,
        )


class BranchUpdate(BranchGetObjectMixin, ClientContextMixin, UpdateView):
    model = Branch
    form_class = BranchForm


class BranchDelete(BranchGetObjectMixin, ClientContextMixin, DeleteView):
    model = Branch

    def get_success_url(self):
        return self.object.client.get_absolute_url()
