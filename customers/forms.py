from accounts.models import User
from django import forms

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phonenumber']
