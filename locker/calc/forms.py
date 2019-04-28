from django import forms
from django.contrib.auth import get_user
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from client.models import Client
from .models import Order, Service, OrderOption


class RelatedFieldWidgetCanAdd(widgets.Select):
    """Append add button to Select widget
    """
    def __init__(self, related_model, related_url=None, *args, **kwargs):
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
        widget=RelatedFieldWidgetCanAdd(Client, related_url="client:create"),
    )

    class Meta:
        model = Order
        exclude = ('author', )

    def save(self, request, commit=True):
        """Переопределено для автоматического
        добавления автора заказа
        """
        order = super().save(commit=False)
        # Если создается новый заказ
        if not order.pk:
            order.author = get_user(request)
        if commit:
            order.save()
            self.save_m2m()
        return order


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class OrderOptionForm(forms.ModelForm):
    class Meta:
        model = OrderOption
        fields = '__all__'
