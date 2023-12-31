# Generated by Django 4.2.6 on 2023-10-13 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0002_alter_citizen_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citizen',
            name='first_name_display',
        ),
        migrations.RemoveField(
            model_name='citizen',
            name='last_name_display',
        ),
        migrations.AddField(
            model_name='citizen',
            name='first_name_low',
            field=models.CharField(blank=True, editable=False, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='citizen',
            name='last_name_low',
            field=models.CharField(blank=True, editable=False, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='first_name',
            field=models.CharField(default='maris', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='citizen',
            name='last_name',
            field=models.CharField(default='maris', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='citizen',
            name='name',
            field=models.CharField(blank=True, editable=False, max_length=254, null=True),
        ),
    ]
