# Generated by Django 5.1.3 on 2024-11-17 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_level_profile_xp'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='total_activities',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_time',
            field=models.IntegerField(default=0),
        ),
    ]
