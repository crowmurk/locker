from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

from client.models import Client, Branch


class OrderCreateClientMixin:
    # Передаваемые в URL аргументы
    client_slug_url_kwarg = 'client_slug'
    branch_pk_url_kwarg = 'branch_pk'
    # Имена переменных для использования в контексте
    client_context_object_name = 'client'
    branch_context_object_name = 'branch'

    def get_context_data(self, **kwargs):
        """Добавляет клиента и объект в контекст заказа
        """
        if hasattr(self, 'client'):
            # Добавляем в контекст имеющися объект
            context = {self.client_context_object_name: self.client, }
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

        if hasattr(self, 'branch'):
            # Добавляем в контекст имеющися объект
            context.update({self.branch_context_object_name: self.branch, })
        else:
            # Извлекаем переданный pk
            branch_pk = self.kwargs.get(self.branch_pk_url_kwarg)
            if branch_pk:
                # Получаем объект
                branch = get_object_or_404(
                    Branch,
                    pk=branch_pk,
                )
                # Добавляем в контекст
                context.update({self.branch_context_object_name: branch, })

        context.update(kwargs)
        return super().get_context_data(**context)

    def get_initial(self):
        """Добавляет клиента и объект в заказ
        """
        initial = dict()

        # Получаем клиента и объект
        client_slug = self.kwargs.get(self.client_slug_url_kwarg)
        branch_pk = self.kwargs.get(self.branch_pk_url_kwarg)

        if client_slug:
            self.client = get_object_or_404(Client, slug__iexact=client_slug)
            # Добавляем к начальным данным представления
            initial.update({self.client_context_object_name: self.client, })

        if branch_pk:
            self.branch = get_object_or_404(Branch, pk=branch_pk)
            # Добавляем к начальным данным представления
            initial.update({self.branch_context_object_name: self.branch, })

        initial.update(self.initial)
        return initial
