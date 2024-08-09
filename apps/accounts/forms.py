from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    referral_code = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "referral_code")


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "bio",
            "location",
            "birth_date",
            "profile_picture",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }
