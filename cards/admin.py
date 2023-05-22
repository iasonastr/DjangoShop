from django.contrib import admin
from .models import Card, CardItem

# Register your models here.

admin.site.register(CardItem)
admin.site.register(Card)
