from django.urls import path, include
from . import views
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.my_account, name='vendor'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
]
