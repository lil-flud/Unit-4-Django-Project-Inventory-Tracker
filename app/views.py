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
# View list of all tires and utilizes search bar function
# TODO: create a non-view view_inventory_fun()?
# authenticated users have permission to edit the tire, buy or sell
# should have a view details for each tire
# authenticated users should have extra links to add tires, view invoices, view outvoices
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


# ===VIEW INVENTORY FUN===
# User can view inventory of their current stock
# Visible fields should be: Brand, Line, Size, Condition, Price, Quantity
# User should be able to select a tire to update the quantity (they cannot update anything else)
# User should be able to filter inventory using a search function
# TODO
# create a search bar that allows user to search by brand, line, size, condition
# this search bar should allow optional searches (ex. user can search by size only, if they like)
# the search bar should refresh the page with the new results
# TODO
# create a means of the user selecting a tire to view details, buy, or sell
# suggestion: on click, go to different view with tire as an argument - tireDetails
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
# this page will allow the user to buy more tires or sell more tires -> send to different view
# render with tire_info.html
# path name = "tire_info"
# TODO: on template, add anchors to buy_tires and sell_tires
def tire_info(request, pk):
    current_tire = Tire.objects.get(id=pk)
    return render(request, "tire_info.html", {"tire": current_tire})
    # From Logan: Fixed tire_info so it correctly displays individual tires.
    # Same style of this solution probably possible for directly updating tire quantities like I mentioned on inventory_base.html and tire_info.html.


# ====BUY TIRES====
# user should be able to select a quantity to buy
# quantity can not be negative
# create_outvoice() on form submit
# TODO: implement
def buy_tires(request, pk):
    context = {}
    return render(request, "buy_tires.html", context)


# ===SELL TIRES=====
# user should be able to select a quantity to sell
# quantity can not be more than the amount of tires in inventory
# create_invoice() on form submit
# TODO: implement
def sell_tires(request, pk):
    context = {}
    return render(request, "sell_tires.html", context)


# ===VIEW INVOICES====
# user should be able to view all details of items of the Invoice model
# TODO: implement
def view_invoices(request):
    context = {}
    return render(request, "view_invoices.html", context)


# ==VIEW OUTVOICES====
# user should be able to view all details of items of the Outvoice model
# TODO: implement
def view_outvoices(request):
    context = {}
    return render(request, "view_outvoices.html", context)


# ====DELETE TIRE====
# user will be able to delete tire
# please add confirmation message before deletion
# TODO: implement
def delete_tire(request):
    context = {}
    return render(request, "delete_tire.html", context)


# ===================USER REGISTRATION AND LOGIN================


def registerView(request):
    context = {}
    return render(request, "register.html", context)


def loginView(request):
    context = {}
    return render(request, "login.html", context)
