from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Tag(models.Model):
#     name = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name


class Store(models.Model):
    store_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.store_name + ", " + self.location


class Tire(models.Model):
    PATTERNS = (
        ("Street Tread", "Street Tread"),
        ("All-Terrain", "All-Terrain"),
        ("Mud Terrain", "Mud-Terrain"),
    )
    CONDITIONS = (
        (1, "Heavily Used"),
        (2, "Used"),
        (3, "Good"),
        (4, "New"),
    )

    brand = models.CharField(max_length=200, null=True)
    line = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=200, null=True)
    mileage_rating = models.CharField(max_length=40, null=True)
    base_price = models.FloatField(null=True)
    tread_pattern = models.CharField(max_length=200, null=True, choices=PATTERNS)
    condition = models.IntegerField(null=True, choices=CONDITIONS)
    adjusted_price = models.FloatField(null=True, blank=True, default=None)
    quantity = models.IntegerField(default=0)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="inventory", null=True, blank=True
    )
    order_qty = models.IntegerField(null=True)
    # invoices
    # outvoices

    # __STR__
    # had to change to strf due to elements being Nonetype and couldn't concatenate

    def __str__(self):
        return f"{self.size} | {self.brand} | {self.line}"

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
    store = models.ForeignKey(
        Store, related_name="outvoices", on_delete=models.CASCADE, null=True
    )
    is_finalized = models.BooleanField(default=False)
    # order_quantity


class OrderQuantity(models.Model):
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, null=True, blank=True)
    num_of_tires = models.IntegerField(null=True)
    outvoice = models.ForeignKey(
        Outvoice,
        related_name="order_quantity",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


def create_outvoice(user, qty, finished, outvoice, store, tire=None):
    if outvoice == None:
        outvoice = Outvoice(user=user)
        outvoice.store = store
        outvoice.save()
    if outvoice.user == "placeholder":
        outvoice.user = user
        outvoice.store = store
        outvoice.save()
    if not finished:
        update_outvoice(outvoice, tire, qty)
    if finished and outvoice.user != "placeholder":
        finalize_outvoice(outvoice)


def update_outvoice(outvoice, tire, qty):
    tire.order_qty += qty
    tire.save()
    outvoice.tires.add(tire)
    outvoice.save()


def finalize_outvoice(outvoice):
    tires = outvoice.tires.all()
    tot_cost = 0.0
    user = User.objects.get(username=outvoice.user)
    for tire in tires:
        if tire not in user.profile.store.inventory.all():
            user.profile.store.inventory.add(tire)
        tire.quantity += tire.order_qty
        tot_cost += tire.base_price * tire.order_qty
        order = OrderQuantity(tire=tire, num_of_tires=tire.order_qty)
        order.save()
        outvoice.order_quantity.add(order)
        # outvoice.order_quantity.tire = tire
        # outvoice.order_quantity.num_of_tires = tire.order_qty
        outvoice.save()
        tire.order_qty = 0
        tire.save()
    outvoice.total_cost = tot_cost
    outvoice.is_finalized = True
    outvoice.save()
    newOutvoice = Outvoice(user="placeholder")
    newOutvoice.save()


def calculate_total_cost(outvoice):
    tires = outvoice.tires.all()
    tot_cost = 0.0
    for tire in tires:
        tot_cost += tire.base_price * tire.order_qty
    return tot_cost


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="staff_members"
    )

    def __str__(self):
        return self.user.username + ", " + self.store.store_name


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


# =======STORES========#
def createStore(store_name, location):
    store = Store(store_name=store_name, location=location)
    store.save()
    return store


def createProfile(user, store):
    profile = Profile(user=user, store=store)
    profile.save()


def getStore(store_name, location):
    try:
        store = Store.objects.all().get(store_name=store_name, location=location)
        return store
    except:
        return None


def delete_tire(tire):
    tire.delete()


def get_tire(pk):
    try:
        tire = Tire.objects.get(id=pk)
        return tire
    except:
        return None
