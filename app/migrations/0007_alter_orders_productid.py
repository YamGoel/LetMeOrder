# Generated by Django 4.2.8 on 2023-12-31 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_payment_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='productid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cart'),
        ),
    ]