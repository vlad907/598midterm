from django import forms
from django.core import validators
from django.contrib.auth.models import User

def validate_position(value):
    if len(value) != 2 or value[0] not in "abcdefgh" or value[1] not in "12345678":
        raise forms.ValidationError("Use standard chess coordinate format, e.g. a1.")

class ChessMoveForm(forms.Form):
    from_position = forms.CharField(
        min_length=2, max_length=2, strip=True,
        widget=forms.TextInput(attrs={'placeholder': 'a1', 'style': 'font-size:small'}),
        validators=[validators.MinLengthValidator(2),
                    validators.MaxLengthValidator(2),
                    validate_position]
    )
    to_position = forms.CharField(
        min_length=2, max_length=2, strip=True,
        widget=forms.TextInput(attrs={'placeholder': 'a1', 'style': 'font-size:small'}),
        validators=[validators.MinLengthValidator(2),
                    validators.MaxLengthValidator(2),
                    validate_position]
    )

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
            'username': None
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
