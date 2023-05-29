from django.contrib import admin
from .models import Card, CardItem


# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'created_at')


class CardItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'card', 'quantity', 'is_active')


admin.site.register(CardItem, CardItemAdmin)
admin.site.register(Card, CardAdmin)
