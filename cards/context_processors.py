from .models import Card, CardItem
from .views import _get_card_id


def counter(request):
    card_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            card = Card.objects.filter(card_id=_get_card_id(request))
            card_items = CardItem.objects.all().filter(card=card[:1])
            for card_item in card_items:
                card_count += card_item.quantity
        except Card.DoesNotExist:
            card_count = 0
        return dict(card_count=card_count)
