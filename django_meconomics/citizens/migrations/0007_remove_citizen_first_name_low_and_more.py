# Generated by Django 4.2.6 on 2023-10-15 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0006_remove_citizen_companies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citizen',
            name='first_name_low',
        ),
        migrations.RemoveField(
            model_name='citizen',
            name='last_name_low',
        ),
        migrations.AddField(
            model_name='citizen',
            name='full_name',
            field=models.CharField(default='m', max_length=254),
            preserve_default=False,
        ),
    ]
