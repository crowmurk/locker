from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from .models import Client
from .forms import ClientForm

# Create your views here.
class ClientList(ListView):
    model = Client
    paginate_by = 7


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
