# Generated by Django 4.2.7 on 2023-11-18 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_remove_warehouse_display_name_warehouse_name_low_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=12)),
                ('location_type', models.CharField(choices=[('0', 'General'), ('1', 'Sales'), ('2', 'RawMat'), ('3', 'Prod'), ('4', 'Internal'), ('5', 'Retail Sale'), ('6', 'Construction Bin')], default='0', max_length=8)),
                ('multi_article', models.BooleanField(default=True)),
                ('block_in', models.BooleanField(default=False)),
                ('block_out', models.BooleanField(default=False)),
                ('capacity', models.IntegerField(blank=True, default=0)),
                ('warehouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loc_warehouse', to='companies.warehouse')),
            ],
        ),
        migrations.AddConstraint(
            model_name='warehouselocation',
            constraint=models.UniqueConstraint(fields=('warehouse', 'code'), name='unique_warehouse_code'),
        ),
    ]
