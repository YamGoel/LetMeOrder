# Generated by Django 4.2.8 on 2024-01-30 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_feedback_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='feed_mail',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='feed_name',
            new_name='name',
        ),
    ]
