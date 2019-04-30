from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Client
from .forms import OrderOptionFormSet

class OrderCreateAddClientInContext:
    # Имя переданного аргумента в URLConf,
    # содержащего значение slug
    client_slug_url_kwarg = 'client_slug'
    # Имя переменной для использования в контексте
    client_context_object_name = 'client'

    def get_context_data(self, **kwargs):
        """Добавляет клиента в контекст заказа
        """
        if hasattr(self, 'client'):
            context = {
                # Добавляем в контекст имеющися объект
                self.client_context_object_name: self.client,
            }
        else:
            # Извлекаем переданный slug
            client_slug = self.kwargs.get(self.client_slug_url_kwarg)
            if client_slug:
                # Получаем объект
                client = get_object_or_404(
                    Client,
                    slug__iexact=client_slug,
                )
                # Добавляем в контекст
                context = {self.client_context_object_name: client, }
            else:
                context = dict()

        context.update(kwargs)
        return super().get_context_data(**context)

    def get_initial(self):
        """Добавляет клиента в заказ
        """
        # Получаем клиента
        client_slug = self.kwargs.get(self.client_slug_url_kwarg)
        if client_slug:
            self.client = get_object_or_404(Client, slug__iexact=client_slug)
            # Добавляем к начальным данным представления
            initial = {self.client_context_object_name: self.client, }
            initial.update(self.initial)
            return initial
        return self.initial


class OrderFormMixin:
    def get_context_data(self, *args, **kwargs):
        """ Добавляет formset в контекст
        создания и изменения закака
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
