# Generated by Django 3.0.5 on 2020-04-24 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0009_remove_profile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]