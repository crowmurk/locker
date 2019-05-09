from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django_xhtml2pdf.views import PdfMixin

from core.views import DeleteColumnMixin

from .models import Order, Service, OrderOption
from .forms import OrderForm, ServiceForm, OrderOptionForm
from .tables import (
    OrderTable,
    OrderCreateServiceTable,
    ServiceTable,
    OrderOptionTable,
)
from .filters import OrderFilter, ServiceFilter, OrderOptionFilter
from .utils import OrderCreateAddClientInContext, OrderFormMixin


class ServiceList(SingleTableMixin, DeleteColumnMixin, FilterView):
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


class OrderList(SingleTableMixin, DeleteColumnMixin, FilterView):
    model = Order
    table_class = OrderTable
    filterset_class = OrderFilter
    template_name = 'calc/order_list.html'


class OrderCreate(OrderCreateAddClientInContext, CreateView):
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data()
        context['table'] = OrderCreateServiceTable(Service.objects.all())
        return context

    def form_valid(self, form):
        """Переопределено для автоматического
        добавления автора заказа  и опций
        """

        if form.is_valid():
            self.object = form.save(self.request)
            pks = self.request.POST.getlist('add')
            if pks:
                for service in Service.objects.filter(pk__in=pks):
                    self.object.services.add(service)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class OrderDetail(DetailView, DeleteColumnMixin):
    model = Order
    related_model = OrderOption
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(object=self.object)
        context['table'] = OrderOptionTable(self.object.get_options(), exclude=('order', ))
        return context


class OrderDetailPDF(PdfMixin, DetailView):
    model = Order
    template_name = "calc/order_detail_pdf.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(object=self.object)
        context['table'] = OrderOptionTable(self.object.get_options(), exclude=('order', ))
        return context


class OrderUpdate(OrderFormMixin, UpdateView):
    model = Order
    form_class = OrderForm


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('calc:order:list')


class OrderOptionList(SingleTableMixin, DeleteColumnMixin, FilterView):
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
