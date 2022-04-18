# Generated by Django 4.0.3 on 2022-04-05 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Financial_Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(blank=True, null=True)),
                ('fy_yr', models.CharField(blank=True, max_length=10, null=True)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('q1_from', models.DateField(blank=True, null=True)),
                ('q1_to', models.DateField(blank=True, null=True)),
                ('q2_from', models.DateField(blank=True, null=True)),
                ('q2_to', models.DateField(blank=True, null=True)),
                ('q3_from', models.DateField(blank=True, null=True)),
                ('q3_to', models.DateField(blank=True, null=True)),
                ('q4_from', models.DateField(blank=True, null=True)),
                ('q4_to', models.DateField(blank=True, null=True)),
                ('h1_from', models.DateField(blank=True, null=True)),
                ('h1_to', models.DateField(blank=True, null=True)),
                ('h2_from', models.DateField(blank=True, null=True)),
                ('h2_to', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cont_State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Global.country')),
            ],
        ),
    ]