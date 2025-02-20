from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from .models import Vendor
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import user_passes_test, check_role_vendor
from menu.models import Category, FoodItem
# Create your views here.

def get_vendor(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Restaurant details updated!. ')
            return redirect('vendor_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=user_profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': user_profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendor_profile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk, vendor=vendor)
    food_items = FoodItem.objects.filter(category=category)
    context = {
        'category': category,
        'food_items': food_items,
    }
    print(food_items, 'food_items')
    return render(request, 'vendor/fooditems_by_category.html', context)
