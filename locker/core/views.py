from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _

# Create your views here.

class ActionTableDeleteMixin:
    """Удаляет записи из таблиц в представлении.

    Для для удаления из БД должна быть задана model в переменной
    action_table_model. Если представление содержит несколько
    таблиц, необходимио в списке action_table_multitables для
    каждой таблице задать словарь содержащий имя модели (ключ
    action_table_model) и имя соответствующей кнопки (ключ
    action_table_button) для обработки нажатия.
    """
    action_table_model = None
    action_table_button = "action-table-button"
    action_table_success_message = None
    action_table_error_message = None
    action_table_multitables = None

    def post(self, request, *args, **kwargs):
        if self.action_table_model:
            # Задана одна таблица
            self.action_table_multitables = [
                {
                    'model': self.action_table_model,
                    'button': self.action_table_button,
                    'success_message': self.action_table_success_message,
                    'error_message': self.action_table_error_message,
                }
            ]
        elif self.action_table_multitables:
            # Задано несолько таблиц
            for action_table in self.action_table_multitables:
                # Должна быть задана как минимум model
                if not action_table.get('model'):
                    raise ImproperlyConfigured(
                        "You must specify model in action_table_multitables"
                        " ({class_name}) to configure {mixin_name}".format(
                            class_name=self.__class__,
                            mixin_name=__class__.__name__,
                        )
                    )
        else:
            # Должна быть задана как минимум model
            raise ImproperlyConfigured(
                "You must specify action_table_model or action_table_multitables"
                " ({class_name}) to configure {mixin_name}".format(
                    class_name=self.__class__,
                    mixin_name=__class__.__name__,
                )
            )

        # Удаляем записи из таблиц
        for action_table in self.action_table_multitables:
            model = action_table['model']
            button = action_table.get('button', self.action_table_button)
            error_message = action_table.get(
                'error_message',
                self.action_table_error_message,
            )
            success_message = action_table.get(
                'success_message',
                self.action_table_success_message,
            )

            # Сообщения по умолчанию
            if not success_message:
                success_message = _("{name} were deleted successfuly").format(
                    name=model._meta.verbose_name_plural
                )

            if not error_message:
                error_message = _("Cannot delete {name} because of"
                                  " foreign references").format(
                                      name=model._meta.verbose_name_plural.lower()
                )

            # Удаляем записи из БД
            button = request.POST.get(button)
            pks = request.POST.getlist(button)
            if pks:
                selected_objects = model.objects.filter(pk__in=pks)
                try:
                    selected_objects.delete()
                    messages.success(request, success_message)
                except ProtectedError:
                    messages.error(request, error_message)

        return HttpResponseRedirect(request.path)


class DeleteMessageMixin:
    """Выводит сообщение о результате удаления записи.
    """
    success_message = None
    error_message = None

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
            if self.success_message:
                success_message = self.success_message
            else:
                success_message = _("{name} was deleted successfuly").format(
                    name=self.model._meta.verbose_name
                )
            # Удаление прошло успешно
            messages.success(self.request, success_message)
        except ProtectedError:
            # Запись защищена от удаления
            if self.error_message:
                error_message = self.error_message
            else:
                error_message = _("Cannot delete {name} because of"
                                  " foreign references").format(
                                      name=self.model._meta.verbose_name.lower()
                )
            messages.error(self.request, error_message)
            return HttpResponseRedirect(self.object.get_absolute_url())
        return result


class SingleFormSetMixin:
    """Добавляет formset в контекст формы.
    """
    formset = None
    paginate_by = None

    def get_context_data(self, *args, **kwargs):
        """ Добавляет formset в контекст.
        """
        if not self.formset:
            raise ImproperlyConfigured(
                "You must specify formset in '{class_name}'"
                " to configure '{mixin_name}'".format(
                    class_name=self.__class__,
                    mixin_name=__class__.__name__,
                )
            )

        context_data = super().get_context_data(*args, **kwargs)

        queryset = self.formset.model.objects.filter(
            **{self.formset.fk.name: self.object}
        )

        # Добавляем paginator
        if self.paginate_by:
            paginator = Paginator(queryset, self.paginate_by)
            page = self.request.GET.get('page')

            try:
                page_objects = paginator.page(page)
            except PageNotAnInteger:
                page_objects = paginator.page(1)
            except EmptyPage:
                page_objects = paginator.page(paginator.num_pages)

            page_query = queryset.filter(
                id__in=[item.id for item in page_objects]
            )

            context_data['paginator'] = page_objects

        # Добавляем formset
        if self.request.method == 'POST':
            context_data['formset'] = self.formset(
                self.request.POST,
                instance=self.object,
            )
        else:
            context_data['formset'] = self.formset(
                instance=self.object,
                queryset=page_query if self.paginate_by else queryset,
            )

        return context_data

    def form_valid(self, form):
        """ Сохраняет formset.
        """
        redirect = super().form_valid(form)
        formset = self.formset(
            self.request.POST,
            instance=self.object,
        )

        if formset.is_valid():
            try:
                formset.save()
            except ProtectedError:
                # Запись защищена от удаления
                error_message = _("Cannot delete {name} because of"
                                  " foreign references").format(
                                      name=formset.model._meta.verbose_name.lower()
                )
                messages.error(self.request, error_message)
            return redirect

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
