# shop/cart/cart.py
from decimal import Decimal
from django.conf import settings
from main.models import Product

# В settings.py должно быть: CART_SESSION_ID = 'cart'
CART_SESSION_ID = getattr(settings, 'CART_SESSION_ID', 'cart')


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if cart is None:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity=1, override_quantity=False):
        """Добавить/обновить товар в корзине."""
        product_id = str(product.id)
        if product_id not in self.cart:
            # ВАЖНО: сохраняем price как str, чтобы сессия (JSON) не падала
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        # Помечаем сессию как изменённую, чтобы Django её сохранил
        self.session.modified = True

    def remove(self, product: Product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Итерируемся по товарам корзины с подмешанными объектами Product и Decimal-ценами."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            pid = str(product.id)
            item = cart[pid]
            item = item.copy()
            item['product'] = product
            # Конвертируем обратно в Decimal перед подсчетами
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()
