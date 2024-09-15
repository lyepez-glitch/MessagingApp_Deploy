

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# creating a form
class SignUpForm(UserCreationForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = User

        # specify fields to be used
        fields = [
            "username",
            "password1",
            "password2"
        ]
class LogInForm(AuthenticationForm):
  pass