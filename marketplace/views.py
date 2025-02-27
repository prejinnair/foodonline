from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
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

    return render(request, 'market_place/vendor_detail.html', {'vendor': vendor})
