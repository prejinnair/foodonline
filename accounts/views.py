from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            messages.success(request, 'Your account has been created successfully')
            return redirect('register_user')
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register_user.html', context)
