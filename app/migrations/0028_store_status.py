# Generated by Django 4.2.8 on 2024-03-06 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_store_store_timings_alter_cart_orderid'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='status',
            field=models.CharField(default='offline', max_length=100),
            preserve_default=False,
        ),
    ]
