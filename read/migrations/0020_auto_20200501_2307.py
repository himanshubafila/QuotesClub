# Generated by Django 3.0.5 on 2020-05-01 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('read', '0019_auto_20200501_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='followers_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following_count', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
