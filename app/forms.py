from django.forms import ModelForm
from app.models import Tire

# TODO
# EXCLUDE UNNECESSARY FIELDS FOR THE FORM
class TireForm(ModelForm):
    class Meta:
        model = Tire
        exclude = ["adjusted_price"]
