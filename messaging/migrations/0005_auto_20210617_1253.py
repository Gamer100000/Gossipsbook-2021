# Generated by Django 3.2.4 on 2021-06-17 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_auto_20210607_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatingroommessage',
            name='chat_room',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ch_messages', to='messaging.chatingroom'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chatingroom',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='chatingroommessage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
