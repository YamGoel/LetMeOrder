# Generated by Django 4.2.8 on 2024-02-02 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_orders_ordernumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(),
        ),
    ]
