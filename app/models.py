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
    invoice = models.ForeignKey(
        "Invoice", null=True, related_name="tire_set", on_delete=models.CASCADE
    )
    outvoice = models.ForeignKey(
        "Outvoice", null=True, related_name="tire_set", on_delete=models.CASCADE
    )

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
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    total_cost = models.FloatField()
    # tire_set


def create_outvoice(user, tires):
    cost = 0.0
    for tire in tires:
        cost = cost = tire.adjust_cost()


class Invoice(models.Model):
    user = models.CharField(max_length=200)
    indv_cost = models.FloatField()
    total_cost = models.FloatField()
    date_sold = models.DateTimeField(auto_now_add=True, null=True)
    # tire


def create_invoice(user, tire, qty):
    cost = tire.adjust_cost()
    tot_cost = cost * qty
    invoice = Invoice(user=user, indv_cost=cost, total_cost=tot_cost)
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
