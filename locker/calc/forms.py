from django import forms

from .models import Order, Service, OrderOption


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class OrderOptionForm(forms.ModelForm):
    class Meta:
        model = OrderOption
        fields = '__all__'
