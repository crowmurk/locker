from django.contrib.auth.decorators import permission_required
from django.urls import path, include

from . import views


app_name = 'calc'

order = [
    path('', views.OrderList.as_view(), name='list'),
    path('estimates.pdf', views.OrderListPDF.as_view(), name='list_pdf'),
    path('create/', views.OrderCreate.as_view(), name='create'),
    path('<int:pk>/', views.OrderDetail.as_view(), name='detail'),
    path('<int:pk>/estimate.pdf', views.OrderDetailPDF.as_view(), name='detail_pdf'),
    path('<int:pk>/update/', views.OrderUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.OrderDelete.as_view(), name='delete'),
]

service = [
    path('', views.ServiceList.as_view(), name='list'),
    path('create/',
         permission_required('is_superuser')(views.ServiceCreate.as_view()),
         name='create'),
    path('<int:pk>/', views.ServiceDetail.as_view(), name='detail'),
    path('<int:pk>/update/',
         permission_required('is_superuser')(views.ServiceUpdate.as_view()),
         name='update'),
    path('<int:pk>/delete/',
         permission_required('is_superuser')(views.ServiceDelete.as_view()),
         name='delete'),
]

orderoption = [
    path('', views.OrderOptionList.as_view(), name='list'),
    path('create/', views.OrderOptionCreate.as_view(), name='create'),
    path('<int:pk>/', views.OrderOptionDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.OrderOptionUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.OrderOptionDelete.as_view(), name='delete'),
]

urlpatterns = [
    path('estimate/', include((order, 'order'))),
    path('equipment/', include((service, 'service'))),
    path('estimateequipment/', include((orderoption, 'orderoption'))),
]
