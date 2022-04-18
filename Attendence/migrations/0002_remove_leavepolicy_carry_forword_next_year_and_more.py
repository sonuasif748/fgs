# Generated by Django 4.0.3 on 2022-04-14 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendence', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavepolicy',
            name='Carry_forword_Next_year',
        ),
        migrations.RemoveField(
            model_name='leavepolicy',
            name='Eligibility_for_leave',
        ),
        migrations.RemoveField(
            model_name='leavepolicy',
            name='Leave_Encashment_pm',
        ),
        migrations.RemoveField(
            model_name='leavepolicy',
            name='No_of_leaves_pa',
        ),
        migrations.RemoveField(
            model_name='leavepolicy',
            name='Type_of_leave',
        ),
        migrations.AddField(
            model_name='leavepolicy',
            name='Custom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Attendence.custom'),
        ),
        migrations.AddField(
            model_name='leavepolicy',
            name='Fac',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Attendence.factoriesact'),
        ),
        migrations.AddField(
            model_name='leavepolicy',
            name='Shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Attendence.shopestablishment'),
        ),
    ]
