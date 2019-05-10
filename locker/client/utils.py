from django.shortcuts import get_object_or_404

from .models import Client, Branch


class ClientContextMixin():
    # Имя переданного аргумента в URLConf,
    # содержащего значение slug
    client_slug_url_kwarg = 'client_slug'
    # Имя переменной для использования в контексте
    client_context_object_name = 'client'

    def get_context_data(self, **kwargs):
        """Добавляет объект Client в контекст представлений Branch
        """
        if hasattr(self, 'client'):
            context = {
                # Добавляем в контекст имеющися объект
                self.client_context_object_name: self.client,
            }
        else:
            # Извлекаем переданный slug
            client_slug = self.kwargs.get(self.client_slug_url_kwarg)
            # Получаем объект
            client = get_object_or_404(
                Client,
                slug__iexact=client_slug,
            )
            # Добавляем в контекст
            context = {self.client_context_object_name: client, }
        context.update(kwargs)
        return super().get_context_data(**context)


class BranchGetObjectMixin():
    def get_object(self, queryset=None):
        """Возвращает объект Branch, который отображается
        представлениями
        """
        # Получаем slug из аргументов переданных представлению
        client_slug = self.kwargs.get(self.client_slug_url_kwarg)
        branch_pk = self.kwargs.get(self.pk_url_kwarg)

        if client_slug is None or branch_pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with "
                "either a client_slug  and a branch_pk."
                % self.__class__.__name__
            )
        return get_object_or_404(
            Branch,
            pk=branch_pk,
            client__slug__iexact=client_slug,
        )
