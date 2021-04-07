import datetime
import re

from django import forms
from django.contrib.auth import get_user
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from client.models import Client

from .models import Order, Service, OrderOption


class CustomDurationField(forms.DurationField):
    def prepare_value(self, value):
        """Removing the milliseconds and
        seconds of the duration field"""

        if isinstance(value, datetime.timedelta):
            seconds = int(value.total_seconds())
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            return '{:d}:{:02d}'.format(hours, minutes)

    def to_python(self, value):
        regex = re.compile(r'^((?P<hours>\d+?):)?'
                           r'(?P<minutes>\d+?)$')

        if value is None or isinstance(value, datetime.timedelta):
            return value

        try:
            parts = regex.match(value)
            if parts:
                kwargs = {
                    item: int(value) for item, value in parts.groupdict().items()
                    if value is not None
                }
                parsed = datetime.timedelta(**kwargs)
            else:
                parsed = None
        except ValueError:
            parsed = None

        if parsed is not None:
            return parsed

        raise ValidationError(
            _('Invalid value: %(value)s'),
            code='invalid',
            params={'value': value},
        )


class ServiceForm(forms.ModelForm):
    work_duration = CustomDurationField(
        label=_('Work duration'),
        help_text=_('Duration time format [HH:]MM'),
    )

    class Meta:
        model = Service
        fields = '__all__'

    def has_changed(self, *args, **kwargs):
        return True


class RelatedFieldWidgetCanAdd(widgets.Select):
    """Append add button to Select widget
    """
    def __init__(self, related_model, *args, related_url=None, **kwargs):
        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kwargs)
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append(
            '&nbsp;<a href="{url}" class="button">{name}</a>'.format(
                url=self.related_url,
                name=_("Create"),
            ),
        )
        return mark_safe(' '.join(output))


class OrderForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        required=True,
        queryset=Client.objects.all(),
        widget=RelatedFieldWidgetCanAdd(
            Client,
            related_url="client:create",
        ),
        label=_('Client'),
    )

    class Meta:
        model = Order
        exclude = ('author', 'services')

    def has_changed(self, *args, **kwargs):
        return True

    def clean(self):
        cleaned_data = super().clean()

        # Заданный объект должен соответвовать клиенту
        client = cleaned_data['client']
        branch = cleaned_data['branch']

        if client != branch.client:
            self.add_error(
                'branch',
                forms.ValidationError(
                    _('%(client)s client does not own'
                      ' %(branch)s (%(address)s) branch'),
                    code='invalid',
                    params={
                        'client': client,
                        'branch': branch.name,
                        'address': ', '.join((branch.settlement, branch.address)),
                    },
                ),
            )

        return cleaned_data

    def save(self, *args, **kwargs):
        """Переопределено для автоматического
        добавления автора заказа
        """
        commit = kwargs.get('commit', True)
        request = kwargs.get('request')

        order = super().save(commit=False)
        # Если создается новый заказ
        if not order.pk:
            if not request:
                raise ValueError(_('Request object required'))
            else:
                order.author = get_user(request)
        if commit:
            order.save()
            self.save_m2m()
        return order


class OrderOptionForm(forms.ModelForm):
    class Meta:
        model = OrderOption
        fields = '__all__'

    def has_changed(self, *args, **kwargs):
        return True


OrderOptionFormSet = inlineformset_factory(
    Order,
    Order.services.through,
    form=OrderOptionForm,
    can_delete=True,
    extra=0,
)
