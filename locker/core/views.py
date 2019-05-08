from django.http import HttpResponseRedirect

# Create your views here.

class DeleteColumnMixin:
    related_model = None
    delete_button = "action-table-delete-button"

    def post(self, request, *args, **kwargs):
        button = request.POST.get(self.delete_button)
        pks = request.POST.getlist(button)
        if pks:
            model = self.related_model if self.related_model else self.model
            selected_objects = model.objects.filter(pk__in=pks)
            selected_objects.delete()
        return HttpResponseRedirect(request.path)
