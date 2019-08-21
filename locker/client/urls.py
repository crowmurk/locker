from django.urls import path, include

from calc.views import OrderCreate

from . import views

app_name = 'client'

branch = [
    path('', views.BranchListClient.as_view(), name='list'),
    path('create/', views.BranchCreate.as_view(), name='create'),
    path('<int:pk>/', views.BranchDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.BranchUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.BranchDelete.as_view(), name='delete'),
    path('<int:branch_pk>/order/create/', OrderCreate.as_view(), name='order_create'),
]

urlpatterns = [
    path('', views.ClientList.as_view(), name='list'),
    path('branch/', views.BranchList.as_view(), name='branch'),
    path('create/', views.ClientCreate.as_view(), name='create'),
    path('<slug:slug>/', views.ClientDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', views.ClientUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', views.ClientDelete.as_view(), name='delete'),
    path('<slug:client_slug>/order/create/', OrderCreate.as_view(), name='order_create'),
    path('<slug:client_slug>/branch/', include((branch, 'branch'))),
]
