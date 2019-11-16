from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import Client, Branch

# Register your models here.

class BranchInline(admin.StackedInline):
    model = Branch
    extra = 0


class ClientResource(ModelResource):
    class Meta:
        model = Client
        exclude = ('slug', )


class ClientAdmin(ImportExportModelAdmin):
    resource_class = ClientResource
    inlines = (BranchInline, )
    list_display = ('name', 'details', 'get_number_of_orders')
    search_fields = ('name', 'details')

    def get_number_of_orders(self, instance):
        return instance.number_of_orders

    get_number_of_orders.short_description = _('Number of estimates')


admin.site.register(Client, ClientAdmin)
