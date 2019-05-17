import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from django.contrib.auth.models import User

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
            content_type="application/json; encoding=utf-8",
        )


class UserListJson(View):
    def get(self, request, *args, **kwargs):
        users = list(map(
            ' '.join,
            User.objects.values_list('first_name', 'last_name'),
        ))
        json_users = json.dumps(users)
        return HttpResponse(
            json_users,
            content_type="application/json; encoding=utf-8")
