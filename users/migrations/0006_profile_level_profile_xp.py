# Generated by Django 5.1.3 on 2024-11-17 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_activity_options_alter_activity_skill_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='xp',
            field=models.IntegerField(default=0),
        ),
    ]