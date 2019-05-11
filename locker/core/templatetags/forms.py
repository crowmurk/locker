from django.template import Library, TemplateSyntaxError

from core.templatetags.names import verbose_name

register = Library()

@register.inclusion_tag(
    'core/includes/filter_table_form.html',
    takes_context=True,
)
def filter_table_form(context, *args, **kwargs):
    """Тег представления filter form как таблицы
    """
    filter_form = context.get('filter')

    if not filter_form:
        filter_form = (args[0] if len(args) > 0
                       else kwargs.get('filter'))

    if filter_form is None:
        raise TemplateSyntaxError(
            "filter_table template tag requires "
            "at least one argument: filter.")

    return {'filter': filter_form, }


@register.inclusion_tag(
    'core/includes/action_table_form.html',
    takes_context=True,
)
def action_table_form(context, *args, **kwargs):
    """Тег формы таблицы с выбираемыми строками
    """
    request = context.get('request')

    table = (args[0] if len(args) > 0
             else kwargs.get('table'))

    if not table:
        table = context.get('table')

    if table is None:
        raise TemplateSyntaxError(
            "action_table template tag requires "
            "at least one argument: table.")

    action = kwargs.get('action', '')
    method = kwargs.get('method', 'post')
    button_type = kwargs.get('button_type', 'submit')
    button_class = kwargs.get('button_class', 'button')
    button_name = kwargs.get('button_name', 'action-table-button')
    button_value = kwargs.get('button_value', 'action-table-column-item')
    action_verbose = kwargs.get('action_verbose', 'Submit')

    return {
        'request': request,
        'action': action,
        'method': method,
        'table': table,
        'button_type': button_type,
        'button_class': button_class,
        'button_name': button_name,
        'button_value': button_value,
        'action_verbose': action_verbose,
    }


@register.inclusion_tag(
    'core/includes/formset_table.html',
    takes_context=True,
)
def formset_table(context, *args, **kwargs):
    """Тег представления formset как таблицы
    """
    formset = context.get('formset')

    if not formset:
        formset = (args[0] if len(args) > 0
                   else kwargs.get('formset'))

    if formset is None:
        raise TemplateSyntaxError(
            "formset_table template tag requires "
            "at least one argument: formset.")

    return {'formset': formset, }


@register.inclusion_tag(
    'core/includes/form.html',
    takes_context=True,
)
def form(context, *args, **kwargs):
    """Тег формы создания и изменения объекта.
    """
    # Формируем контекст для шаблона формы
    request = context.get('request')

    action = (args[0] if len(args) > 0
              else kwargs.get('action'))
    action_verbose = (args[1] if len(args) > 1
                      else kwargs.get('action_verbose'))
    method = (args[2] if len(args) > 2
              else kwargs.get('method'))
    form = context.get('form')
    formset = context.get('formset')
    table = context.get('table')
    view = context.get('view')

    if hasattr(view, 'model'):
        action_verbose = ' '.join(
            [action_verbose,
             verbose_name(view.model).lower()],
        )

    if action is None:
        raise TemplateSyntaxError(
            "form template tag requires "
            "at least one argument: action, "
            "which is a URL.")

    return {
        'request': request,
        'action': action,
        'action_verbose': action_verbose,
        'form': form,
        'formset': formset,
        'table': table,
        'method': method,
    }


@register.inclusion_tag(
    'core/includes/delete_form.html',
    takes_context=True,
)
def delete_form(context, *args, **kwargs):
    """Тег формы удаления объекта.
    """
    # Формируем контекст для шаблона формы
    action = (args[0] if len(args) > 0
              else kwargs.get('action'))
    method = (args[1] if len(args) > 1
              else kwargs.get('method'))
    form = context.get('form')
    display_object = kwargs.get(
        'object', context.get('object'))
    if action is None:
        raise TemplateSyntaxError(
            "delete_form template tag "
            "requires at least one argument: "
            "action, which is a URL.")
    if display_object is None:
        raise TemplateSyntaxError(
            "display_form needs object "
            "manually specified in this case.")
    if hasattr(display_object, 'name'):
        object_name = display_object.name
    else:
        object_name = str(display_object)
    object_type = kwargs.get(
        'obj_type',
        verbose_name(display_object),
    )
    return {
        'action': action,
        'form': form,
        'method': method,
        'object': display_object,
        'object_name': object_name,
        'object_type': object_type,
    }
