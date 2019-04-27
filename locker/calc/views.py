from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponseRedirect

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from .models import Order, Service, OrderOption
from .forms import OrderForm, ServiceForm, OrderOptionForm
from .tables import OrderTable, ServiceTable, OrderOptionTable
from .filters import OrderFilter, ServiceFilter, OrderOptionFilter


class OrderFormValidMixin:
    def form_valid(self, form):
        """Переопределено для автоматического
        добавления автора заказа
        """
        self.object = form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())


class OrderList(SingleTableMixin, FilterView):
    model = Order
    table_class = OrderTable
    filterset_class = OrderFilter
    template_name = 'calc/order_list.html'


class OrderCreate(OrderFormValidMixin, CreateView):
    model = Order
    form_class = OrderForm


class OrderDetail(DetailView):
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(object=self.object)
        context['table'] = OrderOptionTable(self.object.get_options())
        return context


class OrderUpdate(OrderFormValidMixin, UpdateView):
    model = Order
    form_class = OrderForm


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('calc:order:list')


class ServiceList(SingleTableMixin, FilterView):
    model = Service
    table_class = ServiceTable
    filterset_class = ServiceFilter
    template_name = 'calc/service_list.html'


class ServiceCreate(CreateView):
    model = Service
    form_class = ServiceForm


class ServiceDetail(DetailView):
    model = Service
    form_class = ServiceForm


class ServiceUpdate(UpdateView):
    model = Service
    form_class = ServiceForm


class ServiceDelete(DeleteView):
    model = Service
    success_url = reverse_lazy('calc:service:list')


class OrderOptionList(SingleTableMixin, FilterView):
    model = OrderOption
    table_class = OrderOptionTable
    filterset_class = OrderOptionFilter
    template_name = 'calc/orderoption_list.html'


class OrderOptionCreate(CreateView):
    model = OrderOption
    form_class = OrderOptionForm


class OrderOptionDetail(DetailView):
    model = OrderOption
    form_class = OrderOptionForm


class OrderOptionUpdate(UpdateView):
    model = OrderOption
    form_class = OrderOptionForm


class OrderOptionDelete(DeleteView):
    model = OrderOption
    success_url = reverse_lazy('calc:orderoption:list')
