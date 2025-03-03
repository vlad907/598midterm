from django import forms
from django.core import validators
from django.contrib.auth.models import User

def validate_position(value):
    if not (value.startswith("r") and "c" in value and value[1].isdigit() and value[-1].isdigit()):
        raise forms.ValidationError("Use row and column format, e.g. r1c1.")

class ChessMoveForm(forms.Form):
    from_position = forms.CharField(
        min_length=4, max_length=4, strip=True,
        widget=forms.TextInput(attrs={'placeholder': 'r2c1', 'style': 'font-size:small'}),
        validators=[validators.MinLengthValidator(4),
                    validators.MaxLengthValidator(4),
                    validate_position]
    )
    to_position = forms.CharField(
        min_length=4, max_length=4, strip=True,
        widget=forms.TextInput(attrs={'placeholder': 'r4c1', 'style': 'font-size:small'}),
        validators=[validators.MinLengthValidator(4),
                    validators.MaxLengthValidator(4),
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
