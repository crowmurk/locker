from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class SelectWidgetCanAdd(widgets.Select):
    """Append add button to Select widget
    """
    def __init__(self, *args, **kwargs):
        self.related_url = kwargs.pop('related_url', None)
        self.link_class = kwargs.pop('link_class', '')
        self.link_name = kwargs.pop('link_name', _('Add'))
        self.new_tab = kwargs.pop('new_tab', True)
        super().__init__(*args, **kwargs)

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(SelectWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append(
            '<a href="{url}" id="{_id}" class="{link_class}" {new_tab}>{name}</a>'.format(
                url=self.related_url,
                _id=kwargs.get('attrs')['id'] + '_create',
                link_class=self.link_class,
                name=self.link_name,
                new_tab='target="_blank" rel="noopener noreferrer"' if self.new_tab else '',
            ),
        )
        return mark_safe(' '.join(output))


class SelectMultipleWidgetCanAdd(widgets.SelectMultiple, SelectWidgetCanAdd):
    """Append add button to SelectMultiple widget
    """
    pass
