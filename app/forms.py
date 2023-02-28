from django.forms import ModelForm
from app.models import Tire


class TireForm(ModelForm):
    class Meta:
        model = Tire
        fields = "__all__"
