# Generated by Django 4.2.8 on 2024-01-30 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_cart_orderid_alter_cart_product_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feed_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('feed_name', models.CharField(max_length=100)),
                ('feed_mail', models.CharField(max_length=100)),
                ('feedback', models.CharField(max_length=1000)),
            ],
        ),
    ]