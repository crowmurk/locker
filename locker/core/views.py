from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

class ActionTableDeleteMixin:
    action_table_model = None
    action_table_button = "action-table-button"
    action_table_multitables = dict()
    success_delete_message = None

    def post(self, request, *args, **kwargs):
        actions = dict()
        if self.action_table_model:
            actions.update({self.action_table_button: self.action_table_model, })
        actions.update(self.action_table_multitables)

        if not actions:
            raise ImproperlyConfigured(
                "You must specify action_table_model or action_table_multitables"
                " in {class_name} for configure {mixin_name}".format(
                    class_name=self.__class__,
                    mixin_name=__class__.__name__,
                )
            )

        for button_name, model in actions.items():
            button = request.POST.get(button_name)
            pks = request.POST.getlist(button)
            if pks:
                selected_objects = model.objects.filter(pk__in=pks)
                selected_objects.delete()
                if self.success_delete_message:
                    messages.success(self.request, self.success_delete_message)

        return HttpResponseRedirect(request.path)


class SuccessDeleteMessageMixin:
    success_delete_message = None

    def delete(self, request, *args, **kwargs):
        if self.success_delete_message:
            messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
