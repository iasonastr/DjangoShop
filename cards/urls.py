from django.urls import path
from . import views

urlpatterns = [
    path('', views.card, name='card'),
    path('add_card/<int:product_id>/', views.add_card, name='add_card'),
    path('remove_card/<int:product_id>/<int:card_item_id>', views.remove_card, name='remove_card'),
    path('remove_card_item/<int:product_id>/<int:card_item_id>', views.remove_card_item, name='remove_card_item')
]
