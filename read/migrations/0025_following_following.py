# Generated by Django 3.0.5 on 2020-05-03 05:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('read', '0024_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='following',
            name='following',
            field=models.ManyToManyField(related_name='following_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
