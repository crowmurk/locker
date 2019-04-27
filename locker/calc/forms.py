from django import forms
from django.contrib.auth import get_user

from .models import Order, Service, OrderOption


class OrderForm(forms.ModelForm):
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
