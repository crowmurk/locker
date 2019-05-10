from django.urls import path, re_path, include

from calc.views import OrderCreate

from . import views

app_name = 'client'

branch = [
    path('', views.BranchList.as_view(), name='list'),
    path('create/', views.BranchCreate.as_view(), name='create'),
    path('<int:pk>/', views.BranchDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.BranchUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.BranchDelete.as_view(), name='delete'),
]

urlpatterns = [
    path('', views.ClientList.as_view(), name='list'),
    path('create/', views.ClientCreate.as_view(), name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.ClientDetail.as_view(), name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/update/$', views.ClientUpdate.as_view(), name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.ClientDelete.as_view(), name='delete'),
    re_path(r'^(?P<client_slug>[\w-]+)/createorder/$', OrderCreate.as_view(), name='createorder'),
    re_path(r'^(?P<client_slug>[\w-]+)/branch/', include((branch, 'branch'))),
]
