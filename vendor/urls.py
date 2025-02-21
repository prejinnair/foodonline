from django.urls import path, include
from . import views
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.my_account, name='vendor'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
    #Category CRUD
    path('menu_builder/category/add/', views.add_category, name='add_category'),
]
