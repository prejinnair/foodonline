from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import requests
from accounts.models import UserProfile
from django.core.files.base import ContentFile

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """If the email exists, log in. Otherwise, create the user with the defined structure."""
        email = sociallogin.account.extra_data.get("email", "").lower()

        if email:
            try:
                # Check if user with the same email already exists
                existing_user = User.objects.get(email=email, is_active=True)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass  # Allow new user creation

    def populate_user(self, request, sociallogin, data):
        """Create a new user with the defined structure."""
        user = sociallogin.user
        user_field(user, 'first_name', data.get('first_name', ''))
        user_field(user, 'last_name', data.get('last_name', ''))
        user_field(user, 'email', data.get('email', ''))

        # Set username
        user.username = f"{data.get('first_name', '')} {data.get('last_name', '')}".capitalize()
        user.is_active = True
        user.role = 2
        return user

    def save_user(self, request, sociallogin, form=None):
        """Save user and download profile picture if available."""
        user = super().save_user(request, sociallogin, form)

        # Extract profile picture URL from Google
        extra_data = sociallogin.account.extra_data
        profile_picture_url = extra_data.get('picture', None)

        if profile_picture_url:
            # Download the image
            response = requests.get(profile_picture_url)
            if response.status_code == 200:
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                image_name = f"profile_{user.id}.jpg"
                user_profile.profile_picture.save(image_name, ContentFile(response.content), save=True)

        return user
