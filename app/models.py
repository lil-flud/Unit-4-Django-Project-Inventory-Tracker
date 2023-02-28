from django.db import models

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

#__STR__
#had to change to strf due to elements being Nonetype and couldn't concatenate

    def __str__(self):
        return f"{self.size} | {self.brand} | {self.line} | {self.adjusted_price} | {self.quantity}"
#ADJUST COST
#adjust the cost for the tire according to condition
#WORKS
    def adjust_cost(self):
        if self.condition == 4:
            self.adjusted_price = self.base_price
        elif self.condition == 3:
            self.adjusted_price = self.base_price * 0.85
        elif self.condition == 2:
            self.adjusted_price = self.base_price * 0.75
        elif self.condition == 1:
            self.adjusted_price = self.base_price * 0.50
        self.save()

#===GET TIRE===#
#retrieve tire by brand, line, size, condition
#if any error occurs, return none
#else, return the tire
#TODO
#create an exception for if multiple tires are returned
def get_tire(brand, line, size, condition):
    try:
        tire = Tire.objects.get(brand=brand, line=line, size=size, condition=condition)
    except:
        return None
    else:
        return tire

#TODO
#test this function 
def update_quantity(brand,line,size,condition,quantity):
    tire = get_tire(brand,line,size,condition)
    tire.quantity = quantity
    return tire