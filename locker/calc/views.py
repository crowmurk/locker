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

from django_xhtml2pdf.views import PdfMixin

from .models import Order, Service, OrderOption
from .forms import OrderForm, ServiceForm, OrderOptionForm, OrderOptionFormSet
from .tables import OrderTable, ServiceTable, OrderOptionTable
from .filters import OrderFilter, ServiceFilter, OrderOptionFilter

#    def get(self, request, *args, **kwargs):
#        """ Создает пустую форму
#        """
#        self.object = None
#        form_class = self.get_form_class()
#        form = self.get_form(form_class)
#        option_form = self.options_form_set()
#        return self.render_to_response(
#            self.get_context_data(
#                form=form,
#                option_form=option_form,
#            ),
#        )
#
#    def post(self, request, *args, **kwargs):
#        """ Создает экземпляр формы с данными переданными
#        через запрос и проверят их
#        """
#        self.object = None
#        form_class = self.get_form_class()
#        form = self.get_form(form_class)
#        option_form = self.options_form_set(self.request.POST)
#        if (form.is_valid() and option_form.is_valid()):
#            return self.form_valid(form, option_form)
#        else:
#            return self.form_invalid(form, option_form)
#
#    def form_valid(self, form, option_form):
#        """Переопределено для автоматического добавления автора
#        и создания форм опций заказа
#        """
#        self.object = form.save(self.request)
#        option_form.instance = self.object
#        option_form.save()
#        return HttpResponseRedirect(self.get_success_url())
#
#    def form_invalid(self, form, option_form):
#        """Пересоздает данные контекста с данными форм и ошибками
#        """
#        return self.render_to_response(
#            self.get_context_data(form=form,
#                                  option_form=option_form,
#                                  ),
#        )

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


class OrderFormMixin:
    def get_context_data(self, *args, **kwargs):
        """ Добавляет formset в контекст
        """
        context_data = super().get_context_data(*args, **kwargs)

        if self.request.method == 'POST':
            context_data['formset'] = OrderOptionFormSet(
                self.request.POST,
                instance=self.object,
                prefix='order_options'
            )
        else:
            context_data['formset'] = OrderOptionFormSet(
                instance=self.object,
                prefix='order_options'
            )
        return context_data

    def form_valid(self, form):
        """Переопределено для автоматического
        добавления автора заказа  и опций
        """
        context_data = self.get_context_data()
        formset = context_data['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save(self.request)
            instances = formset.save(commit=False)

            for item in formset.deleted_objects:
                item.delete()

            for item in instances:
                item.order = self.object
                item.save()

            formset.save_m2m()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class OrderList(SingleTableMixin, FilterView):
    model = Order
    table_class = OrderTable
    filterset_class = OrderFilter
    template_name = 'calc/order_list.html'


class OrderCreate(OrderFormMixin, CreateView):
    model = Order
    form_class = OrderForm


class OrderDetail(DetailView):
    model = Order
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
