from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from employee.models import Profile

# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'last_name', 'first_name', 'get_middle_name', 'is_staff', 'is_active')

    def get_middle_name(self, instance):
        return instance.profile.middle_name

    get_middle_name.short_description = _('Middle name')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
