from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from .models import Order, Service, OrderOption
from .forms import OrderForm, ServiceForm, OrderOptionForm


class OrderList(ListView):
    model = Order
    paginate_by = 7


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm


class OrderDetail(DetailView):
    model = Order
    form_class = OrderForm


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('calc:order:list')


class ServiceList(ListView):
    model = Service
    paginate_by = 7


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


class OrderOptionList(ListView):
    model = OrderOption
    paginate_by = 7


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
