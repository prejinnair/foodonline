from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.market_place, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    path('add_to_cart/<int:food_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:food_id>', views.remove_from_cart, name='remove_from_cart'),
    path('delete_cart_item/<int:cart_id>', views.delete_cart_item, name='delete_cart_item'),
]
