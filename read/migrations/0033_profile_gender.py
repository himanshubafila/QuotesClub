# Generated by Django 3.0.5 on 2020-05-08 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0032_auto_20200507_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(default=' ', max_length=10),
        ),
    ]
