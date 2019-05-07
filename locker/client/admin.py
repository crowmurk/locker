from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Client

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'details', 'get_number_of_orders')
    search_fields = ('name', 'details')

    def get_number_of_orders(self, instance):
        return instance.number_of_orders

    get_number_of_orders.short_description = _('Number of orders')


admin.site.register(Client, ClientAdmin)
