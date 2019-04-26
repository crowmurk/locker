from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableView

from .models import Client
from .tables import ClientTable
from .forms import ClientForm


# Create your views here.
class ClientList(SingleTableView):
    model = Client
    table_class = ClientTable


class ClientCreate(CreateView):
    model = Client
    form_class = ClientForm


class ClientDetail(DetailView):
    model = Client
    form_class = ClientForm


class ClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm


class ClientDelete(DeleteView):
    model = Client
    success_url = reverse_lazy('client:list')
