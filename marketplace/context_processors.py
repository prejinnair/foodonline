from .models import Cart, Tax
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
    tax_dict = {}

    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for item in cart_items:
                    food_item = FoodItem.objects.get(id=item.fooditem.id)
                    sub_total += (food_item.price * item.quantity)
            taxes = Tax.objects.filter(is_active=True)
            for t in taxes:
                tax_type = t.tax_type
                tax_percentage = t.tax_percentage
                tax_amount = round((tax_percentage * sub_total) / 100, 2)
                tax_dict.update({tax_type: {str(tax_percentage): tax_amount}})

            tax = sum(x for tax_info in tax_dict.values() for x in tax_info.values())
            grand_total = sub_total + tax
        except:
            pass
    return dict(sub_total=sub_total, tax=tax, grand_total=grand_total, tax_dict=tax_dict)
