# Generated by Django 4.2.7 on 2023-11-12 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0009_alter_citizen_post_code'),
        ('companies', '0011_companyemployees'),
    ]

    operations = [
        migrations.CreateModel(
            name='GovInstEmployees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=254)),
                ('salary_brutto', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('salary_vsaoi_dd', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('salary_vsaoi_dn', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('salary_iin', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('salary_netto', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('gov_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gov_employer', to='companies.govinstitution')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gov_employee', to='citizens.citizen')),
            ],
        ),
    ]
