from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import Order, Service, OrderOption

# Register your models here.

class OrderOptionInline(admin.StackedInline):
    model = OrderOption
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderOptionInline, )
    list_display = (
        'id',
        'get_author',
        'client',
        'created',
        'modified',
        'factor',
        'get_price',
    )
    search_fields = ('author__last_name', 'client__name',)

    def get_price(self, instance):
        return instance.price

    get_price.short_description = _('Price')

    def get_author(self, instance):
        return instance.author.get_full_name()

    get_author.short_description = _('Author')


class ServiceResource(ModelResource):
    class Meta:
        model = Service


class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource
    list_display = (
        'rating',
        'equipment',
        'equipment_price',
        'work',
        'work_price',
    )
    list_display_links = ('equipment', )
    search_fields = ('equipment', 'work')


admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
