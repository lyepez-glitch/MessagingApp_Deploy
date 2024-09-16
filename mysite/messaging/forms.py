

from django import forms
from django.contrib.auth.models import User
from .models import Profile,Message
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

class ProfileForm(forms.ModelForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = Profile

        fields = [
            "bio",
            "location",
            "phone_number",
            "profile_picture"
        ]
class MessageForm(forms.ModelForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = Message

        fields = [
            "content",
            "receiver"
        ]