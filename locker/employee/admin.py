from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

from employee.models import Profile

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _('Profile')
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = (
        'username',
        'last_name',
        'first_name',
        'get_middle_name',
        'is_superuser',
        'is_staff',
        'is_active',
        'last_login',
    )
    list_filter = (
        'is_superuser',
        'is_staff',
        'is_active',
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('last_name', 'first_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('last_name', 'first_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'is_staff')}),
    )

    readonly_fields = ('last_login', 'date_joined')

    def get_middle_name(self, instance):
        return instance.profile.middle_name

    get_middle_name.short_description = _('Middle name')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
