# urls.py in your app

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create_expense/', views.create_expense, name='create_expense'),
    path('passbook/<int:participant_id>/', views.get_passbook, name='get_passbook'),
]
