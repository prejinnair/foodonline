from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_account, name=''),
    path('register-user/', views.register_user, name='register-user'),
    path('register-vendor/', views.register_vendor, name='register-vendor'),
    path('login/', views.login, name='login'),
    path('my-account/', views.my_account, name='my-account'),
    path('logout/', views.logout, name='logout'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor-dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('vendor/', include('vendor.urls')),
    path('customer/', include('customers.urls')),
]
