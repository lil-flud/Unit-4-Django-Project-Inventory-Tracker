from django.shortcuts import render, redirect
from app.forms import TireForm
from app.models import *
from app import models
from .decorators import unauthenticated_user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from app.forms import *
from app.models import *
from app import models
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import re
from dataclasses import dataclass
from typing import List

# Create your views here.


# ===HOME VIEW===#
# Landing page
# View list of all tires and utilizes search bar function
# authenticated users have permission to edit the tire, buy or sell
# should have a view details for each tire
# authenticated users should have extra links to add tires, view invoices, view outvoices
# Logan: I've got a lot of the searchability down, still need to do the size search.
@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def home(request):
    profile = Profile.objects.get(user=request.user)
    tires_all = Tire.objects.filter(store=profile.store)
    # current_user = request.user
    logged_in_check = logged_in_check_function(request)
    size_filter = sorted(
        list(set(profile.store.inventory.values_list("size", flat=True)))
    )
    brand_filter = sorted(
        list(set(profile.store.inventory.values_list("brand", flat=True)))
    )
    line_filter = sorted(
        list(set(profile.store.inventory.values_list("line", flat=True)))
    )
    tread_pattern_filter = sorted(
        list(set(profile.store.inventory.values_list("tread_pattern", flat=True)))
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
        filtered_tire_list = profile.store.inventory.filter(**q)

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
@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def add_tire(request):
    profile = Profile.objects.get(user=request.user)
    form = TireForm()
    successMessage = ""
    errorMessage = ""
    context = {"form": form}
    if request.method == "POST":
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
                quantity = form.cleaned_data["order_qty"]
                condition = form.cleaned_data["condition"]
                tire = models.get_tire(brand, line, size, condition)
                store = request.user.profile.store
                try:
                    outvoice = Outvoice.objects.latest("id")
                except:
                    outvoice = None
                if tire == None:
                    form.save()
                    formtire = models.get_tire(brand, line, size, condition)
                    formtire.adjust_cost()
                    formtire.save()
                    # profile.store.inventory.add(formtire)
                    create_outvoice(
                        request.user.username,
                        formtire.quantity,
                        False,
                        outvoice,
                        store,
                        formtire,
                    )
                elif tire != None:
                    tire.save()
                    profile.store.inventory.add(tire)
                    create_outvoice(
                        request.user.username,
                        tire.quantity,
                        False,
                        outvoice,
                        store,
                        tire,
                    )
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


# ===TIRE INFO VIEW===#
# user will view specific selected tire
# this page will allow the user to buy more tires or sell more tires -> send to different view
# render with tire_info.html
# path name = "tire_info"
# TODO: button to delete tires
@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def tire_info(request, pk):
    current_tire = get_tire(pk)
    if current_tire == None:
        return render(
            request, "tire_info.html", {"doesNotExist": "This tire does not exist"}
        )
    user = request.user.username
    context = {"tire": current_tire}
    store = request.user.profile.store
    if request.method == "POST":
        tires_sold = request.POST.get("tires_sold")
        tires_bought = request.POST.get("tires_bought")
        if tires_bought:
            tires_bought = int(tires_bought)
            try:
                outvoice = Outvoice.objects.latest("id")
            except:
                outvoice = None
            create_outvoice(user, tires_bought, False, outvoice, store, current_tire)

            current_tire.save()
        if tires_sold:
            tires_sold = int(tires_sold)
            current_tire.quantity -= tires_sold
            create_invoice(user, current_tire, tires_sold)
            current_tire.save()
        context["testtext"] = tires_bought
    return render(request, "tire_info.html", context)
    # From Logan: Fixed tire_info so it correctly displays individual tires.
    # Same style of this solution probably possible for directly updating tire quantities like I mentioned on inventory_base.html and tire_info.html.


@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def show_cart(request):
    context = {}
    try:
        outvoice = Outvoice.objects.latest("id")
        tires = outvoice.tires.all()
        context["outvoice"] = outvoice
        context["tires"] = tires
        if not tires:
            context["message"] = "Cart is Empty"

    except:
        pass
    else:
        if request.method == "POST":
            create_outvoice("placeholder", 0, True, outvoice, None)
            return redirect("home")
    return render(request, "cart.html", context)


# ====BUY TIRES====
# user should be able to select a quantity to buy
# quantity can not be negative
# create_outvoice() on form submit
# TODO: implement
@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def buy_tires(request, pk):
    context = {}
    return render(request, "buy_tires.html", context)


# ===SELL TIRES=====
# user should be able to select a quantity to sell
# quantity can not be more than the amount of tires in inventory
# create_invoice() on form submit
# TODO: implement
@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def sell_tires(request, pk):
    context = {}
    return render(request, "sell_tires.html", context)


# ===VIEW INVOICES====
# user should be able to view all details of items of the Invoice model
# TODO: implement
@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def view_invoices(request):
    invoices = Invoice.objects.all()
    context = {"invoices": invoices}
    return render(request, "view_invoices.html", context)


# ==VIEW OUTVOICES====
# user should be able to view all details of items of the Outvoice model
# TODO: implement
@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def view_outvoices(request):
    outvoices = Outvoice.objects.filter(store=request.user.profile.store)

    context = {"outvoices": outvoices}
    return render(request, "view_outvoices.html", context)


# ====DELETE TIRE====
# user will be able to delete tire
# please add confirmation message before deletion
@login_required(login_url="login")
@allowed_users(allowed_roles="staff")
def delete_tirePage(request, pk):
    tire = get_tire(pk)
    context = {"tire": tire}
    if tire == None:
        context[
            "message"
        ] = "This tire does not exist or was removed from the database."
    if request.method == "POST":
        answer = request.POST.get("delete").lower()
        if answer == "yes":
            delete_tire(tire)
            context["tire"] = get_tire(pk)
            context["message"] = "Tire successfully deleted."
    return render(request, "delete_tire.html", context)


# ===================USER REGISTRATION AND LOGIN================


@unauthenticated_user
def registerView(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            store_name = form.cleaned_data["store"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"].upper()
            store_location = city + ", " + state
            form.save()
            user = User.objects.all().last()
            store = getStore(store_name, store_location)
            if store == None:
                store = createStore(store_name, store_location)
            createProfile(user, store)
            group = Group.objects.get(name="staff")
            user.groups.add(group)
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
    messages.info(request, "You have successfully logged out")
    return redirect("login")


# =======EXTRA FUNCTIONS AND CHECKS=======#


@login_required
def logged_in_check_function(request):
    logged_in_check = False
    if request.user in User.objects.all():
        logged_in_check = True
    return logged_in_check
