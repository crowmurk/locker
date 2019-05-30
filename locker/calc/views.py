from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django_xhtml2pdf.views import PdfMixin

from core.views import ActionTableDeleteMixin, SuccessDeleteMessageMixin

from .models import Order, Service, OrderOption
from .forms import OrderForm, ServiceForm, OrderOptionForm
from .tables import (
    OrderTable,
    OrderCreateServiceTable,
    ServiceTable,
    OrderOptionTable,
)
from .filters import OrderFilter, ServiceFilter, OrderOptionFilter
from .utils import OrderCreateClientMixin, OrderFormMixin


class ServiceList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Service
    table_class = ServiceTable
    filterset_class = ServiceFilter
    template_name = 'calc/service_list.html'
    action_table_model = Service
    action_table_success_message = _("Services were deleted successfuly")


class ServiceCreate(CreateView):
    model = Service
    form_class = ServiceForm


class ServiceDetail(DetailView):
    model = Service
    form_class = ServiceForm


class ServiceUpdate(UpdateView):
    model = Service
    form_class = ServiceForm


class ServiceDelete(SuccessDeleteMessageMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('calc:service:list')
    success_message = _("Service was deleted successfuly")


class OrderList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Order
    table_class = OrderTable
    filterset_class = OrderFilter
    template_name = 'calc/order_list.html'
    action_table_model = Order
    action_table_success_message = _("Orders were deleted successfuly")


class OrderListPDF(PdfMixin, OrderList):
    template_name = "calc/order_list_pdf.html"

    def get_table_kwargs(self):
        return {
            'exclude': ('delete', ),
            'order_by': 'id',
        }


class OrderCreate(OrderCreateClientMixin, SingleTableMixin, CreateView):
    model = Order
    table_class = OrderCreateServiceTable
    form_class = OrderForm

    def get_table_data(self):
        return Service.objects.all()

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


class OrderDetail(SingleTableMixin, ActionTableDeleteMixin, DetailView):
    model = Order
    table_class = OrderOptionTable
    form_class = OrderForm
    action_table_model = OrderOption
    action_table_success_message = _("Order's options were deleted successfuly")

    def get_table_data(self):
        return self.object.get_options()

    def get_table_kwargs(self):
        return {'exclude': ('order',), }


class OrderDetailPDF(PdfMixin, OrderDetail):
    template_name = "calc/order_detail_pdf.html"

    def get_table_kwargs(self):
        return {'exclude': ('order', 'delete', ), }


class OrderUpdate(SuccessMessageMixin, OrderFormMixin, UpdateView):
    model = Order
    form_class = OrderForm
    paginate_by = 10
    success_message = _("Order was changed successfuly")


class OrderDelete(SuccessDeleteMessageMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('calc:order:list')
    success_message = _("Order was deleted successfuly")


class OrderOptionList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = OrderOption
    table_class = OrderOptionTable
    filterset_class = OrderOptionFilter
    template_name = 'calc/orderoption_list.html'
    action_table_model = OrderOption
    action_table_success_message = _("Orders' options were deleted successfuly")


class OrderOptionCreate(CreateView):
    model = OrderOption
    form_class = OrderOptionForm


class OrderOptionDetail(DetailView):
    model = OrderOption
    form_class = OrderOptionForm


class OrderOptionUpdate(UpdateView):
    model = OrderOption
    form_class = OrderOptionForm


class OrderOptionDelete(SuccessDeleteMessageMixin, DeleteView):
    model = OrderOption
    success_url = reverse_lazy('calc:orderoption:list')
    success_message = _("Order's option was deleted successfuly")
