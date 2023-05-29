from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, CardItem
from products.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _get_card_id(request):
    card = request.session.session_key
    if not card:
        card = request.session.create()
    return card


def remove_card(request, product_id, card_item_id):
    card = Card.objects.get(card_id=_get_card_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        card_item = CardItem.objects.get(product=product, card=card, id=card_item_id)
        if card_item.quantity > 1:
            card_item.quantity -= 1
            card_item.save()
        else:
            card_item.delete()
    except:
        pass
    return redirect('card')


def remove_card_item(request, product_id, card_item_id):
    card = Card.objects.get(card_id=_get_card_id(request))
    product = get_object_or_404(Product, id=product_id)
    card_item = CardItem.objects.get(product=product, card=card, id=card_item_id)
    card_item.delete()
    return redirect('card')


def add_card(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            print(item)

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        card = Card.objects.get(card_id=_get_card_id(request))
    except ObjectDoesNotExist:
        card = Card.objects.create(
            card_id=_get_card_id(request)
        )
    card.save()

    is_card_item_exists = CardItem.objects.filter(product=product, card=card).exists()

    if is_card_item_exists:
        card_item = CardItem.objects.filter(product=product, card=card)
        ex_var_list = []
        id = []
        for item in card_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        if product_variation in ex_var_list:
            idx = ex_var_list.index(product_variation)
            item_id = id[idx]
            item = CardItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CardItem.objects.create(product=product, quantity=1, card=card)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        card_item = CardItem.objects.create(
            product=product,
            quantity=1,
            card=card, )
        if len(product_variation) > 0:
            card_item.variations.clear()
            card_item.variations.add(*product_variation)
        card_item.save()
    return redirect('card')


def card(request, total=0, quantity=0, card_items=None):
    tax = 0
    grand_total = 0
    try:
        card = Card.objects.get(card_id=_get_card_id(request))
        card_items = CardItem.objects.filter(card=card, is_active=True)
        for card_item in card_items:
            total += (card_item.product.price * card_item.quantity)
            quantity += card_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except Card.DoesNotExist:
        pass

    context = {
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'quantity': quantity,
        'card_items': card_items,
        'currency': '€'
    }
    return render(request, 'store/card.html', context)
