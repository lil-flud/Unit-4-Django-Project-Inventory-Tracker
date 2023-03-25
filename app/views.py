from django.shortcuts import render, redirect
from app.forms import TireForm
from app.models import *
from app import models
from .decorators import unauthenticated_user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from app.forms import *
from app.models import *
from app import models
from .decorators import unauthenticated_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import re

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
# Logan: I've got a lot of the searchability down, still need to do the size search.
def home(request):
    tires_all = Tire.objects.all()
    # current_user = request.user
    logged_in_check = logged_in_check_function(request)
    size_filter = sorted(list(set(Tire.objects.values_list("size", flat=True))))
    brand_filter = sorted(list(set(Tire.objects.values_list("brand", flat=True))))
    line_filter = sorted(list(set(Tire.objects.values_list("line", flat=True))))
    tread_pattern_filter = sorted(
        list(set(Tire.objects.values_list("tread_pattern", flat=True)))
    )
    tire_list = []
    tire_list_len_check = False

    if request.method == "POST":
        searched_size = request.POST["size"]
        searched_brand = request.POST["brand"]
        searched_line = request.POST["line"]
        searched_tread_pattern = request.POST["tread_pattern"]

        q = {}
        if searched_size != "None":
            q.update({"size": searched_size})
        if searched_brand != "None":
            q.update({"brand": searched_brand})
        if searched_line != "None":
            q.update({"line": searched_line})
        if searched_tread_pattern != "None":
            q.update({"tread_pattern": searched_tread_pattern})
        filtered_tire_list = Tire.objects.filter(**q)

        if len(q) == 0 and len(filtered_tire_list) == 0 or len(filtered_tire_list) == 0:
            tire_list_len_check = True

        context = {
            "tire_list_len_check": tire_list_len_check,
            "brands": brand_filter,
            "lines": line_filter,
            "tread_patterns": tread_pattern_filter,
            "tires": filtered_tire_list,
            "logged_in": logged_in_check,
        }
        return render(request, "home.html", context)
    else:
        context = {
            "tires": tires_all,
            "brands": brand_filter,
            "lines": line_filter,
            "tread_patterns": tread_pattern_filter,
            "logged_in": logged_in_check,
        }
        return render(request, "home.html", context)


# ===ADD TIRE VIEW====
# Allows user to add a tire to their inventory
# IMPORTANT: if tire of same brand, model, and size is already in inventory, that tire should update the quantity instead of adding a new tire
# IMPORTANT: on form.save(), be sure to adjust the cost as well according to tire condition using tireobject.adjust_cost()
# render with forms_page.html
# path name = "add_tire_form"
@login_required
def add_tire(request):
    form = TireForm()
    successMessage = ""
    errorMessage = ""
    context = {"form": form}
    if request.method == "POST":
        # print(request.POST)
        form = TireForm(request.POST)
        if form.is_valid():
            # lucas adjustment
            brand = form.cleaned_data["brand"]
            line = form.cleaned_data["line"]
            size = form.cleaned_data["size"]
            # call correct pattern to check file format
            if not correct_pattern(size):
                pass
            else:
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
                successMessage = "Tire successfully added"
                context["successMessage"] = successMessage
        else:
            errorMessage = "There was a problem adding a new tire."
            context["errorMessage"] = errorMessage

    # test_ob = Tire.objects.get(id=3)
    # test = test_ob.condition + 1
    # print(test, test_ob.condition)
    return render(request, "add_tire.html", context)


# ====CORRECT PATTERN====#
# formatting of size must be in XXX-XX-XX format with numbers only
# saving of tire should fail if this returns false
def correct_pattern(string):
    return (
        bool(re.match("[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", string))
        or bool(re.match("[0-9][0-9] x [0-9][0-9].[0-9][0-9]-[0-9][0-9]", string))
        or bool(re.match("[0-9].[0-9][0-9] x [0-9]", string))
    )


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
@login_required
def buy_tires(request, pk):
    context = {}
    return render(request, "buy_tires.html", context)


# ===SELL TIRES=====
# user should be able to select a quantity to sell
# quantity can not be more than the amount of tires in inventory
# create_invoice() on form submit
# TODO: implement
@login_required
def sell_tires(request, pk):
    context = {}
    return render(request, "sell_tires.html", context)


# ===VIEW INVOICES====
# user should be able to view all details of items of the Invoice model
# TODO: implement
@login_required
def view_invoices(request):
    context = {}
    return render(request, "view_invoices.html", context)


# ==VIEW OUTVOICES====
# user should be able to view all details of items of the Outvoice model
# TODO: implement
@login_required
def view_outvoices(request):
    context = {}
    return render(request, "view_outvoices.html", context)


# ====DELETE TIRE====
# user will be able to delete tire
# please add confirmation message before deletion
# TODO: implement
@login_required
def delete_tire(request):
    context = {}
    return render(request, "delete_tire.html", context)


# ===================USER REGISTRATION AND LOGIN================


@unauthenticated_user
def registerView(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = {"form": form}
    return render(request, "register.html", context)


@unauthenticated_user
def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form": form})

def logoutView(request):
    logout(request)
    messages.info(request, 'You have successfully logged out')
    return redirect('home')


# =======EXTRA FUNCTIONS AND CHECKS=======#


@login_required
def logged_in_check_function(request):
    logged_in_check = False
    if request.user in User.objects.all():
        logged_in_check = True
    return logged_in_check
