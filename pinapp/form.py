from django import forms

from .models import UserProfile, Pin


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "bio"]


class PinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ["title", "description", "image"]
