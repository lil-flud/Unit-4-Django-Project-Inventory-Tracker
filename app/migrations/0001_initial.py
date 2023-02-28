# Generated by Django 4.1.5 on 2023-02-28 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("brand", models.CharField(max_length=200, null=True)),
                ("line", models.CharField(max_length=200, null=True)),
                ("size", models.CharField(max_length=200, null=True)),
                ("mileage_rating", models.CharField(max_length=40, null=True)),
                ("base_price", models.FloatField(null=True)),
                (
                    "tread_pattern",
                    models.CharField(
                        choices=[
                            ("Street Tread", "Street Tread"),
                            ("All-Terrain", "All-Terrain"),
                            ("Mud Terrain", "Mud-Terrain"),
                        ],
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "condition",
                    models.IntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True
                    ),
                ),
                (
                    "adjusted_price",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                ("quantity", models.IntegerField(default=0)),
            ],
        ),
    ]