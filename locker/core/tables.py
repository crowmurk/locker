from django.utils.html import mark_safe

import django_tables2 as tables
from django_tables2.utils import AttributeDict


class CheckBoxDeleteColumn(tables.CheckBoxColumn):
    script = {
        'script_name': 'toggle_rows',
        'header_name': 'delete-table-items-header',
        'selection_name': 'delete-table-items',
        'selection_type': 'checkbox',
        'button_name': 'delete-table-items-button',
        'button_type': 'submit'
    }

    def __init__(self, script=dict(), **kwargs):
        self.script.update(script)
        super(CheckBoxDeleteColumn, self).__init__(**kwargs)

    @property
    def header(self):
        default = {
            'name': self.script.get('header_name'),
            'type': self.script.get('selection_type'),
            'onclick': '{script_name}(this,'
            ' {{selectionName: "{selection_name}",'
            ' selectionType: "{selection_type}",'
            ' buttonName: "{button_name}",'
            ' buttonType: "{button_type}"}})'.format(
                script_name=self.script.get('script_name'),
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
            'onclick': '{script_name}(undefined,'
            ' {{selectionName: "{selection_name}",'
            ' selectionType: "{selection_type}",'
            ' buttonName: "{button_name}",'
            ' buttonType: "{button_type}"}})'.format(
                script_name=self.script.get('script_name'),
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
