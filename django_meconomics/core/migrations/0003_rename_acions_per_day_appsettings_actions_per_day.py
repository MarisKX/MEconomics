# Generated by Django 4.2.6 on 2023-10-17 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_appsettings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appsettings',
            old_name='acions_per_day',
            new_name='actions_per_day',
        ),
    ]
