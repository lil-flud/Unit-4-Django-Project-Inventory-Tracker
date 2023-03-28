from django.forms import ModelForm
from app.models import Tire
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# TODO
# EXCLUDE UNNECESSARY FIELDS FOR THE FORM
class TireForm(ModelForm):
    class Meta:
        model = Tire
        exclude = ["adjusted_price", "store", "quantity"]


class CreateUserForm(UserCreationForm):
    STORECHOICES = [
        ("Southern Tire Mart", "Southern Tire Mart"),
        ("Floyd's Tire", "Floyd's Tire"),
        ("Walmart Tire Center", "Walmart Tire Center"),
    ]
    store = forms.ChoiceField(choices=STORECHOICES, required=True)
    city = forms.CharField(max_length=30)
    state = forms.CharField(max_length=2)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
