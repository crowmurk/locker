from django.urls import path, re_path

from . import views


app_name = 'client'

urlpatterns = [
    path('', views.ClientList.as_view(), name='list'),
    path('create/', views.ClientCreate.as_view(), name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.ClientDetail.as_view(), name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/update/$', views.ClientUpdate.as_view(), name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.ClientDelete.as_view(), name='delete'),
]
