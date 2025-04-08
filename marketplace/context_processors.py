from .models import Cart
from django.conf import settings
from menu.models import FoodItem

def get_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for item in cart_items:
                    cart_count += item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amount(request):
    sub_total = 0
    tax = 0
    grand_total = 0

    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for item in cart_items:
                    food_item = FoodItem.objects.get(id=item.fooditem.id)
                    sub_total += (food_item.price * item.quantity)
                grand_total = sub_total + tax
        except:
            pass
    return dict(sub_total=sub_total, tax=tax, grand_total=grand_total)
