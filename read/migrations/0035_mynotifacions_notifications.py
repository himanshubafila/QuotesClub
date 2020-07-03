# Generated by Django 3.0.5 on 2020-05-19 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('read', '0034_blocking_myblocking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('purpose', models.CharField(choices=[('F', 'Follow'), ('L', 'Like'), ('C', 'Comment'), ('S', 'Save')], max_length=1)),
                ('My_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Me', to=settings.AUTH_USER_MODEL)),
                ('post', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='read.Post')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyNotifacions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noti_count', models.IntegerField(default=0)),
                ('notifcations', models.ManyToManyField(blank=True, related_name='Notify', to='read.Notifications')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
