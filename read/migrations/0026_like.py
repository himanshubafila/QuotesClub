# Generated by Django 3.0.5 on 2020-05-03 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('read', '0025_following_following'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_count', models.IntegerField(default=0)),
                ('liker', models.ManyToManyField(blank=True, related_name='like_user', to=settings.AUTH_USER_MODEL)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='read.Post')),
            ],
        ),
    ]
