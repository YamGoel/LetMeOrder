# Generated by Django 4.2.8 on 2024-02-04 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_rename_store_city_store_store_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedorders',
            name='order_date',
            field=models.DateField(),
        ),
    ]