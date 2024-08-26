from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    image = forms.ImageField(label="Profile Image",required=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "image")


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField()
    image = forms.ImageField(label="Profile Image",required=False)
    
    class Meta:
        model = User
        fields = ('username', 'image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("password"):
            password_help_text = (
                "You can change the password " '<a href="{}">here</a>.'
            ).format(f"{reverse('accounts:change_password')}")
            self.fields["password"].help_text = password_help_text

class CustopPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='이전비밀번호')
