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
            # lucas adjustment
            brand = form.cleaned_data["brand"]
            line = form.cleaned_data["line"]
            size = form.cleaned_data["size"]
            quantity = form.cleaned_data["quantity"]
            tire = Tire.objects.filter(brand=brand, line=line, size=size)
            if len(tire) == 0:
                form.adjusted_cost = form.adjust_cost()  # dont know if will work
                form.save()
            elif len(tire) == 1:
                tire.quantity += quantity
                tire.save()
            else:
                raise ValueError("Too many tires")
    context = {"form": form}
    test_ob = Tire.objects.get(id=3)
    test = test_ob.condition + 1
    print(test, test_ob.condition)
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


#TODO
#SEARCH VIEW
#Should search for tires given parameters
#return context with found tires
#render with search.html
def search_view(request):
    return ...
