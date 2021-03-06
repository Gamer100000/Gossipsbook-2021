# Generated by Django 3.2.4 on 2021-06-20 03:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210619_1454'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gossips', '0004_auto_20210617_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='gossipsmodel',
            name='circle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circle_gossips', to='users.circle'),
        ),
        migrations.AlterField(
            model_name='gossipsmodel',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gossip_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
