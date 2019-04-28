from django.contrib import admin

from calc.models import Order

from .models import Client

# Register your models here.

class OrderInline(admin.StackedInline):
    model = Order
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    inlines = (OrderInline, )


admin.site.register(Client, ClientAdmin)
