from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CardAddProductForm

# Делаем функциональное представление. Не классовое, так как проект не большой
# Добавили category_slug=None для указания, что фильровать нам ничего не надо
def product_list(request, category_slug=None):
    categories = Category.objects.all() # Выводим все категории
    products = Product.objects.filter(available=True) # Выводим все доступные продукты

    category = None
    if category_slug: # Если у нас в запросе идёт slug, значит пользователь хочет отфильтровать.
        category = get_object_or_404(Category, slug=category_slug) # Мы берём категорию, что указал пользователь.
        products = products.filter(category=category) # И выводим все продукты в этой категории.
        # Но благодаря get_object_or_404 если такой категории нет, то выведет 404, а не ошибку.

    return render(request, 'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})
    # Мы указали что мы будем выводить в шаблоне. Но не забываем создать шаблоны.

# Делаем страницу самого товара. Обращаться к нему будем по его id и по его slug
def product_detail(request, id, slug):
    # Пользователь заходит и делает запрос с таким id/таким slug. Обрабатываем есть ли они в списке тех, что доступны.
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category,
                                               available=True).exclude(id=product.id)[:4]

    cart_product_form = CardAddProductForm()

    return render(request, 'main/product/detail.html', {'product': product,
                                                        'related_products': related_products,
                                                        'cart_product_form': cart_product_form
                                                        })
