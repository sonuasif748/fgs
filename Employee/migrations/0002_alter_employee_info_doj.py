# Generated by Django 4.0.3 on 2022-04-07 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_info',
            name='doj',
            field=models.DateField(blank=True, null=True, unique=True),
        ),
    ]
