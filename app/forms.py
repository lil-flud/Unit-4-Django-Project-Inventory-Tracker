from django.forms import ModelForm
from app.models import Tire
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# TODO
# EXCLUDE UNNECESSARY FIELDS FOR THE FORM
class TireForm(ModelForm):
    class Meta:
        model = Tire
        exclude = ["adjusted_price"]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
