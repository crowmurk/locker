from django.contrib import admin

from .models import Order, Service, OrderOption

# Register your models here.

class OrderOptionInline(admin.StackedInline):
    model = OrderOption
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderOptionInline, )


class ServiceAdmin(admin.ModelAdmin):
    inlines = (OrderOptionInline, )


admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
