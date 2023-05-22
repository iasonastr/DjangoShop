from django.urls import path
from . import views

urlpatterns = [
    path('', views.card, name='card')
]
