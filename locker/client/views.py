from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableView, SingleTableMixin, MultiTableMixin
from django_filters.views import FilterView

from core.views import ActionTableDeleteMixin, DeleteMessageMixin
from calc.tables import OrderTable
from calc.models import Order

from .models import Client, Branch
from .tables import ClientTable, BranchTable
from .forms import ClientForm, BranchForm
from .filters import ClientFilter, BranchFilter
from .utils import ClientContextMixin, BranchGetObjectMixin


class ClientList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Client
    table_class = ClientTable
    table_pagination = False
    filterset_class = ClientFilter
    template_name = 'client/client_list.html'
    action_table_model = Client
    action_table_success_message = _("Clients were deleted successfuly")


class ClientCreate(CreateView):
    model = Client
    form_class = ClientForm


class ClientDetail(MultiTableMixin, ActionTableDeleteMixin, DetailView):
    model = Client
    form_class = ClientForm
    action_table_multitables = [
        {
            'model': Order,
            'button': 'action-table-button',
            'success_message': _("Estimates were deleted successfuly"),
        },
        {
            'model': Branch,
            'button': 'branch-table-button',
            'success_message': _("Branches were deleted successfuly"),
        },
    ]

    def get_tables(self):
        orders = self.object.get_orders()
        orders_exclude_columns = ['client', ]

        if not self.request.user.is_superuser:
            orders = orders.filter(author=self.request.user)
            orders_exclude_columns.append('author')

        self.tables = [
            OrderTable(orders, exclude=orders_exclude_columns),
            BranchTable(self.object.get_branches(), exclude=('client', )),
        ]
        tables = super(ClientDetail, self).get_tables()
        return tables


class ClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm


class ClientDelete(DeleteMessageMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:list')
    success_message = _("Client was deleted successfuly")


class BranchList(
        SingleTableMixin,
        ActionTableDeleteMixin,
        FilterView,
):
    model = Branch
    table_class = BranchTable
    table_pagination = False
    filterset_class = BranchFilter
    template_name = 'client/branch_list.html'
    action_table_model = Branch
    action_table_button = 'branch-table-button'
    action_table_success_message = _("Branches were deleted successfuly")


class BranchListClient(
        BranchGetObjectMixin,
        ClientContextMixin,
        SingleTableView,
        ActionTableDeleteMixin,
):
    model = Branch
    table_class = BranchTable
    template_name = 'client/branch_list.html'
    action_table_model = Branch
    action_table_button = 'branch-table-button'
    action_table_success_message = _("Branches were deleted successfuly")

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
    table_class = OrderTable
    table_pagination = False
    action_table_model = Order
    action_table_success_message = _("Estimates were deleted successfuly")

    def get_table_kwargs(self):
        kwargs = {
            'exclude': ['client', 'branch', 'settlement', 'address', ]
        }

        if not self.request.user.is_superuser:
            kwargs['exclude'].append('author')

        return kwargs

    def get_table_data(self):
        client_slug = self.kwargs.get(self.client_slug_url_kwarg)
        data_filter = {
            'client__slug__iexact': client_slug,
            'branch': self.object,
        }

        if not self.request.user.is_superuser:
            data_filter['author'] = self.request.user

        return self.action_table_model.objects.filter(**data_filter)


class BranchUpdate(BranchGetObjectMixin, ClientContextMixin, UpdateView):
    model = Branch
    form_class = BranchForm


class BranchDelete(
        BranchGetObjectMixin,
        ClientContextMixin,
        DeleteMessageMixin,
        DeleteView,
):
    model = Branch
    success_message = _("Branch was deleted successfuly")

    def get_success_url(self):
        return self.object.client.get_absolute_url()
