from django.shortcuts import render
from app.forms import TireForm
from app.models import *

# Create your views here.

choices = ["View Inventory", "Add Tire"]


def home(request):
    context = {"choices": choices}
    return render(request, "home.html", context)


def add_tire(request):
    form = TireForm()
    if request.method == "POST":
        # print(request.POST)
        form = TireForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form": form}
    # test_ob = Tire.objects.get(id=3)
    # test = test_ob.condition + 1
    # print(test, test_ob.condition)
    return render(request, "forms_page.html", context)


def view_inventory(request):
    tires = Tire.objects.all()
    for tire in tires:
        print(tire)
    context = {
        "tires": tires,
    }
    return render(request, "inventory_base.html", context)


def tire_info(request, tire):
    current_tire = Tire.objects.filter()
    print(tire)

    return render(request, "tire_info.html", {"tire": tire})
