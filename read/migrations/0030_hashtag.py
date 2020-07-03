# Generated by Django 3.0.5 on 2020-05-06 13:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('read', '0029_auto_20200504_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(default=' ', max_length=20)),
                ('post_count', models.IntegerField(default=0)),
                ('followers_count', models.IntegerField(default=0)),
                ('followers', models.ManyToManyField(blank=True, related_name='follower_user', to=settings.AUTH_USER_MODEL)),
                ('tag_posts', models.ManyToManyField(blank=True, related_name='posts', to='read.Post')),
            ],
        ),
    ]
