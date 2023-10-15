# urls.py in your app

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('find_expense/', views.index, name='find_expense'),
    path('create_expense/', views.create_expense, name='create_expense'),
]
