from django.urls import path, include

from . import views


app_name = 'calc'

order = [
    path('', views.OrderList.as_view(), name='list'),
    path('create/', views.OrderCreate.as_view(), name='create'),
    path('<int:pk>/', views.OrderDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.OrderUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.OrderDelete.as_view(), name='delete'),
    path('<int:pk>/order.pdf', views.OrderDetailPDF.as_view(), name='pdf')
]

service = [
    path('', views.ServiceList.as_view(), name='list'),
    path('create/', views.ServiceCreate.as_view(), name='create'),
    path('<int:pk>/', views.ServiceDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.ServiceUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.ServiceDelete.as_view(), name='delete'),
]

orderoption = [
    path('', views.OrderOptionList.as_view(), name='list'),
    path('create/', views.OrderOptionCreate.as_view(), name='create'),
    path('<int:pk>/', views.OrderOptionDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.OrderOptionUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.OrderOptionDelete.as_view(), name='delete'),
]

urlpatterns = [
    path('order/', include((order, 'order'))),
    path('service/', include((service, 'service'))),
    path('orderoption/', include((orderoption, 'orderoption'))),
]
