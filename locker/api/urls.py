from django.urls import path, include

from . import views

app_name = 'api'

urlpatterns = [
    path('client/<int:pk>/branch/json/', views.ClientBranchJson.as_view(), name='branch_json'),
]
