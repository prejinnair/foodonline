from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detect_user, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify

# Restrict the vendor from accessing the customer dashboard
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the Customer from accessing the vendor dashboard
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('my-account')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            # send verification email
            subject = 'Activate your account'
            template = 'accounts/email/activate_email.html'
            send_verification_email(request, user, subject, template)
            messages.success(request, 'Your account has been created successfully')
            return redirect('register-user')
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register_user.html', context)

def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('my-account')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.RESTAURANT
            user.set_password(password)
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor_name=vendor_form.cleaned_data['vendor_name']
            vendor.vendor_slug = f'{slugify(vendor_name)}-{user.id}'
            vendor.user_profile = user_profile
            vendor.save()
            # send verification email
            subject = 'Activate your account'
            template = 'accounts/email/activate_email.html'
            send_verification_email(request, user, subject, template)
            messages.success(request, 'Your account has been created successfully!, Please wait for the approval.')
            return redirect('register-vendor')
    else:
        form = UserForm()
        vendor_form = VendorForm
    context = {
        'form': form,
        'vendor_form': vendor_form
    }
    return render(request, 'accounts/register_vendor.html', context)

def activate(request, uidb64, token):
    # Activate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! ')
        return redirect('my-account')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('my-account')

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('my-account')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f'Succesfully Logged In as {request.user.username}.')
            return redirect('my-account')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out now.')
    return redirect('login')

@login_required(login_url='login')
def my_account(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    return render(request, 'accounts/vendor_dashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).exists()
        if user:
            user = User.objects.get(email__exact=email)
            # Send a reset password link to the user's email
            subject = 'Reset Your Password'
            template = 'accounts/email/reset_password_email.html'
            send_verification_email(request, user, subject, template)
            messages.success(request, 'Password reset link sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'Account with this email does not exist.')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # Validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else: 
            messages.error(request, 'Password doesnot match!')
            return redirect('reset_password')

    return render(request, 'accounts/reset_password.html')
