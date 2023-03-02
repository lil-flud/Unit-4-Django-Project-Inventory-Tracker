from django.shortcuts import render
from app.forms import TireForm
from app.models import *
from app import models

# Create your views here.

# TODO
# BE SURE TO ADD BACK BUTTON ON ALL HTML PAGES
# IT CAN GO BACK TO HOME, OR WHEREVER


# ===HOME VIEW===#
# Landing page
# allows user to select the option of see their current inventory or add a tire to their stock
# Both options lead to a different page with a different view
# render with home.html
# path name = "home"
def home(request):

    choices = ["View Inventory", "Add Tire"]
    context = {"choices": choices}
    return render(request, "home.html", context)


# ===ADD TIRE VIEW====
# Allows user to add a tire to their inventory
# IMPORTANT: if tire of same brand, model, and size is already in inventory, that tire should update the quantity instead of adding a new tire
# IMPORTANT: on form.save(), be sure to adjust the cost as well according to tire condition using tireobject.adjust_cost()
# render with forms_page.html
# path name = "add_tire_form"
# TODO
# Test if update quantity works (a simple print in the terminal will help with testing) -WORKS
# Test if adjust cost works (a simple print in the terminal will help with testing) -WORKS
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
            condition = form.cleaned_data["condition"]
            tire = models.get_tire(brand, line, size, condition)
            if tire == None:
                form.save()
                formtire = models.get_tire(brand, line, size, condition)
                formtire.adjust_cost()
                formtire.save()
            elif tire:
                tire.quantity += quantity
                tire.save()
                print(tire)
    context = {"form": form}
    # test_ob = Tire.objects.get(id=3)
    # test = test_ob.condition + 1
    # print(test, test_ob.condition)
    return render(request, "forms_page.html", context)


# ===VIEW INVENTORY VIEW===
# User can view inventory of their current stock
# Visible fields should be: Brand, Line, Size, Condition, Price, Quantity
# User should be able to select a tire to update the quantity (they cannot update anything else)
# User should be able to filter inventory using a search function
# render with inventory_base.html
# path name = "inventory"
# TODO
# create a search bar that allows user to search by brand, line, size, condition
# this search bar should allow optional searches (ex. user can search by size only, if they like)
# the search bar should refresh the page with the new results
# TODO
# create a means of the user selecting a tire to update the quantity
# suggestion: on click, go to different view with tire as an argument? --> tire info
def view_inventory(request):
    tires = Tire.objects.all()
    for tire in tires:
        print(tire)
    context = {
        "tires": tires,
    }
    return render(request, "inventory_base.html", context)


# ===TIRE INFO VIEW===#
# user will view specific selected tire
# this page will allow the user to change the quantity of the tire (the user cannot change anything else)
# be sure to add confirmation message
# render with tire_info.html
# path name = "tire_info"
# TODO
# allow user to see chosen tire as chosen from view_inventory view on inventory_base.html
# allow user to update the quantity
# update_quanity() should be in models.py
# create confirmation message and refresh page with new quantity


def tire_info(request, pk):
    current_tire = Tire.objects.get(id=pk)
    return render(request, "tire_info.html", {"tire": current_tire})
    # From Logan: Fixed tire_info so it correctly displays individual tires.
    # Same style of this solution probably possible for directly updating tire quantities like I mentioned on inventory_base.html and tire_info.html.
