# Generated by Django 4.0.3 on 2022-04-08 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0002_alter_employee_info_doj'),
        ('Payroll', '0007_alter_empmonthctcmaster_emp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empmonthctcmaster',
            name='emp_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee.employee_info', unique=True),
        ),
    ]
