from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_count
from django.contrib.auth.decorators import login_required

# Create your views here.

def market_place(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'market_place/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems', queryset = FoodItem.objects.filter(is_available=True))
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items
    }
    return render(request, 'market_place/vendor_detail.html', context)

def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            # check food item exists
            try:
                food_item = FoodItem.objects.get(id=food_id)
                # check if food item is already added to cart
                try:
                    check_cart = Cart.objects.get(fooditem=food_item, user=request.user)
                    # if food item is already added, increment quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status':'Success', 'message': 'Increased cart quantity.', 'cart_count': get_cart_count(request), 'qty': check_cart.quantity})
                except Cart.DoesNotExist:
                    # if food item is not added, create new cart item
                    check_cart = Cart.objects.create(fooditem=food_item, user=request.user, quantity=1)
                    return JsonResponse({'status':'Success', 'message': 'Food Item added to cart.', 'cart_count': get_cart_count(request), 'qty': check_cart.quantity})
            except FoodItem.DoesNotExist:
                return JsonResponse ({'status':'Failed', 'message': 'Food item doesnot exist'})
        else:
            return JsonResponse ({'status':'Failed', 'message': 'Invalid request'})
    return JsonResponse ({'status':'login_required', 'message': 'Please login to continue'})

def remove_from_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check food item exists
            try:
                food_item = FoodItem.objects.get(id=food_id)
                # check if food item is already added to cart
                try:
                    check_cart = Cart.objects.get(fooditem=food_item, user=request.user)
                    # if food item quantity is greater than one, decrement quantity
                    if check_cart.quantity > 1:
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        # if food item quantity is one, delete cart item
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({'status':'Success', 'cart_count': get_cart_count(request), 'qty': check_cart.quantity})
                except Cart.DoesNotExist:
                    return JsonResponse({'status': 'Failed', 'message': 'Food item does not exist in cart.'})
            except FoodItem.DoesNotExist:
                return JsonResponse ({'status':'Failed', 'message': 'Food item doesnot exist'})
        else:
            return JsonResponse ({'status':'Failed', 'message': 'Invalid request'})
    return JsonResponse ({'status':'login_required', 'message': 'Please login to continue'})

@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'market_place/cart.html', context)

def delete_cart_item(request, cart_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(id=cart_id, user=request.user)
                cart_item.delete()
                return JsonResponse({'status':'Success', 'message':'Cart item has been deleted.', 'cart_count': get_cart_count(request)})
            except Cart.DoesNotExist:
                return JsonResponse({'status':'Failed', 'message':'Cart item does not exist.'})
        else:
            return JsonResponse ({'status':'Failed', 'message': 'Invalid request'})
    return JsonResponse({'status':'login_required', 'message':'Please login to continue'})
