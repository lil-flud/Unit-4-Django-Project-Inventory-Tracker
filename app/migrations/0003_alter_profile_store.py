# Generated by Django 4.1.5 on 2023-03-27 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_tire_store"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="store",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="staff_members",
                to="app.store",
            ),
        ),
    ]