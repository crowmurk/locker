from django.utils.html import mark_safe

import django_tables2 as tables
from django_tables2.utils import AttributeDict


class CheckBoxActionColumn(tables.CheckBoxColumn):
    """Добавляет к таблице столбец для выделения строк:

    Параметр script настраивает js скрипт для множественного
    выделения строк:

        function_name - имя функции в скрипте
            (скрипт должен присутствовать в шаблоне)
        header_name - значение name элемента в заголовке таблицы
        selection_name - значение name элементов столбца выделения
        selection_type - тип элементов столбца выделения

    Если таблица используется в форме с кнопкой возможно задать
    параметры кнопки для управления её состоянием (включена/выключена).
    Если хотя бы один из параметров undefined - кнопка отсутствует:

        button_name - параметр name кнопки
        button_type - параметр type кнопки
    """
    def __init__(self, script=dict(), **kwargs):
        self.script = {
            'function_name': 'select_rows',
            'header_name': 'action-table-column-header',
            'selection_name': 'action-table-column-item',
            'selection_type': 'checkbox',
            'button_name': 'undefined',
            'button_type': 'submit'
        }
        self.script.update(script)
        super(CheckBoxActionColumn, self).__init__(**kwargs)

    @property
    def header(self):
        default = {
            'name': self.script.get('header_name'),
            'type': self.script.get('selection_type'),
            'onclick': '{function_name}(this,'
            ' {{selectionName: "{selection_name}",'
            ' selectionType: "{selection_type}",'
            ' buttonName: "{button_name}",'
            ' buttonType: "{button_type}"}})'.format(
                function_name=self.script.get('function_name'),
                selection_name=self.script.get('selection_name'),
                selection_type=self.script.get('selection_type'),
                button_name=self.script.get('button_name'),
                button_type=self.script.get('button_type'),
            ),
        }

        general = self.attrs.get("input")
        specific = self.attrs.get("th__input")
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe("<input %s/>" % attrs.as_html())

    def render(self, value, bound_column, record):
        default = {
            'name': self.script.get('selection_name'),
            'type': self.script.get('selection_type'),
            'value': value,
            'onclick': '{function_name}(undefined,'
            ' {{selectionName: "{selection_name}",'
            ' selectionType: "{selection_type}",'
            ' buttonName: "{button_name}",'
            ' buttonType: "{button_type}"}})'.format(
                function_name=self.script.get('function_name'),
                selection_name=self.script.get('selection_name'),
                selection_type=self.script.get('selection_type'),
                button_name=self.script.get('button_name'),
                button_type=self.script.get('button_type'),
            ),
        }

        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe("<input %s/>" % attrs.as_html())
