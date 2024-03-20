from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput


class UserRegisterForm(UserCreationForm):
    username = TextInput(attrs={'required': True})
    password1 = TextInput(attrs={'required': True})
    password2 = TextInput(attrs={'required': True})

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
