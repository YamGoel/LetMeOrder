# Generated by Django 4.2.8 on 2024-01-02 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_orders_product_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='productid',
            new_name='orderid',
        ),
    ]