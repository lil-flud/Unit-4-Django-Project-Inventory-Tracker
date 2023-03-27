from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Tag(models.Model):
#     name = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name


class Tire(models.Model):
    PATTERNS = (
        ("Street Tread", "Street Tread"),
        ("All-Terrain", "All-Terrain"),
        ("Mud Terrain", "Mud-Terrain"),
    )
    CONDITIONS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    brand = models.CharField(max_length=200, null=True)
    line = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=200, null=True)
    mileage_rating = models.CharField(max_length=40, null=True)
    base_price = models.FloatField(null=True)
    tread_pattern = models.CharField(max_length=200, null=True, choices=PATTERNS)
    condition = models.IntegerField(null=True, choices=CONDITIONS)
    adjusted_price = models.FloatField(null=True, blank=True, default=None)
    quantity = models.IntegerField()
    order_qty = models.IntegerField(null=True)
    # invoices
    # outvoices

    # __STR__
    # had to change to strf due to elements being Nonetype and couldn't concatenate

    def __str__(self):
        return f"{self.size} | {self.brand} | {self.line} | {self.adjusted_price} | {self.quantity}"

    # ADJUST COST
    # adjust the cost for the tire according to condition
    # WORKS
    def adjust_cost(self):
        if self.condition == 4:
            self.adjusted_price = (self.base_price * 0.95) + self.base_price
        elif self.condition == 3:
            self.adjusted_price = (self.base_price * 0.85) + self.base_price
        elif self.condition == 2:
            self.adjusted_price = (self.base_price * 0.75) + self.base_price
        elif self.condition == 1:
            self.adjusted_price = (self.base_price * 0.50) + self.base_price
        self.save()


class Outvoice(models.Model):
    user = models.CharField(max_length=200)

    total_cost = models.FloatField(null=True)
    tires = models.ManyToManyField(Tire, related_name="outvoices")
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)


def create_outvoice(user, qty, finished, outvoice, tire=None):
    if outvoice == None:
        outvoice = Outvoice(user=user)
        outvoice.save()
    if outvoice.user == "placeholder":
        outvoice.user = user
        outvoice.save()
    if not finished:
        update_outvoice(outvoice, tire, qty)
    if finished and user != "placeholder":
        finalize_outvoice(outvoice)


def update_outvoice(outvoice, tire, qty):
    tire.order_qty += qty
    tire.save()
    outvoice.tires.add(tire)
    outvoice.save()


def finalize_outvoice(outvoice):
    tires = outvoice.tires.all()
    tot_cost = 0.0
    for tire in tires:
        tire.quantity += tire.order_qty
        tot_cost += tire.adjusted_price * tire.order_qty
        # tire.order_qty = 0
        tire.save()
    outvoice.total_cost = tot_cost
    outvoice.save()
    newOutvoice = Outvoice(user="placeholder")
    newOutvoice.save()


class Invoice(models.Model):
    user = models.CharField(max_length=200)
    quantity = models.IntegerField(null=True)
    indv_cost = models.FloatField(null=True)
    total_cost = models.FloatField(null=True)
    tires = models.ManyToManyField(Tire, related_name="invoices")
    date_sold = models.DateTimeField(auto_now_add=True, null=True)


def create_invoice(user, tire, qty):
    cost = tire.adjusted_price
    tot_cost = cost * qty
    invoice = Invoice(user=user, quantity=qty, indv_cost=cost, total_cost=tot_cost)
    invoice.save()
    invoice.tires.add(tire)
    invoice.save()


# ===GET TIRE===#
# retrieve tire by brand, line, size, condition
# if any error occurs, return none
# else, return the tire
# TODO
# create an exception for if multiple tires are returned
def get_tire(brand, line, size, condition):
    try:
        tire = Tire.objects.get(brand=brand, line=line, size=size, condition=condition)
    except:
        return None
    else:
        return tire


# TODO
# test this function
def update_quantity(brand, line, size, condition, quantity):
    tire = get_tire(brand, line, size, condition)
    tire.quantity = quantity
    return tire
