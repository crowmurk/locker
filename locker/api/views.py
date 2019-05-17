from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from client.models import Client, Branch

# Create your views here.

class ClientBranchJson(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        client = get_object_or_404(
            Client,
            pk=pk
        )
        branches = Branch.objects.all().filter(client=client)
        json_branches = serializers.serialize(
            "json",
            branches,
        )
        return HttpResponse(
            json_branches,
            content_type="application/json; encoding=utf-8")
