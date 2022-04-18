# Generated by Django 4.0.3 on 2022-04-15 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendence', '0004_delete_factoriesact_delete_shopestablishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavepolicy',
            name='Carry_forword_Next_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leavepolicy',
            name='Eligibility_for_leave',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leavepolicy',
            name='Leave_Encashment_pm',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leavepolicy',
            name='No_of_leaves_pa',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leavepolicy',
            name='Type_of_leave',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
