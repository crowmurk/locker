from django.urls import path, include

from . import views

app_name = 'api'

client = [
    path('<int:pk>/branch/json/', views.ClientBranchJson.as_view(), name='branch_json'),
]

calc = [
]

urlpatterns = [
    path('user/autocomplete', views.UserListJson.as_view(), name='user_autocomplete'),
    path('client/', include((client, 'client'))),
    path('calc/', include((calc, 'calc'))),
]
