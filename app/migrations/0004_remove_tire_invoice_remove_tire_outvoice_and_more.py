# Generated by Django 4.1.5 on 2023-03-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_invoice_outvoice_total_cost_alter_tire_outvoice_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tire",
            name="invoice",
        ),
        migrations.RemoveField(
            model_name="tire",
            name="outvoice",
        ),
        migrations.AddField(
            model_name="invoice",
            name="quantity",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="invoice",
            name="tires",
            field=models.ManyToManyField(related_name="invoices", to="app.tire"),
        ),
        migrations.AddField(
            model_name="outvoice",
            name="tires",
            field=models.ManyToManyField(related_name="outvoices", to="app.tire"),
        ),
    ]
