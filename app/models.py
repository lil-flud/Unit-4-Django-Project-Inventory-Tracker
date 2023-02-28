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
    adjusted_price = models.FloatField(null=True, blank=True, default = None)
    quantity = models.IntegerField()

    def __str__(self):
        return self.size + " " + self.brand + " " + self.line
    
    def adjust_cost(self):
        if self.condition == 4:
            self.adjusted_price = self.base_price
        elif self.condition == 3:
            self.adjusted_price = self.base_price*.85
        elif self.condition == 2:
            self.adjusted_price = self.base_price*.75
        elif self.condition == 1:
            self.adjusted_price = self.base_price*.50
        self.save()
