from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cards.views import CardItem, _get_card_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if len(keyword) > 0:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)


# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_card = CardItem.objects.filter(card__card_id=_get_card_id(request), product=single_product).exists()
        # return HttpResponse(in_card)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_card': in_card
    }
    return render(request, 'store/product_detail.html', context)
