# Generated by Django 4.0.3 on 2022-04-13 11:47

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Employee', '0002_alter_employee_info_doj'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type_of_leave', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('Eligibility_for_leave', models.IntegerField(blank=True, null=True)),
                ('No_of_leaves_pa', models.IntegerField(blank=True, null=True)),
                ('Leave_Encashment_pm', models.FloatField(blank=True, null=True)),
                ('Carry_forword_Next_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeShifts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Year', models.CharField(blank=True, max_length=4, null=True)),
                ('Month', models.CharField(blank=True, max_length=10, null=True)),
                ('shift_name', models.CharField(blank=True, max_length=50, null=True)),
                ('min_start_time', models.TimeField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('max_start_time', models.TimeField(blank=True, null=True)),
                ('min_end_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('max_end_time', models.TimeField(blank=True, null=True)),
                ('break_time', models.TimeField(blank=True, null=True)),
                ('working_days', models.CharField(blank=True, max_length=50, null=True)),
                ('shift_start', models.DateField(blank=True, null=True)),
                ('shift_end', models.DateField(blank=True, null=True)),
                ('weekoffs', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=30, null=True)),
                ('indefnite', models.BooleanField(default=False)),
                ('year_end', models.DateField(blank=True, null=True)),
                ('emp_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employee.employee_info')),
            ],
        ),
        migrations.CreateModel(
            name='FactoriesAct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type_of_leave', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('Eligibility_for_leave', models.IntegerField(blank=True, null=True)),
                ('No_of_leaves_pa', models.IntegerField(blank=True, null=True)),
                ('Leave_Encashment_pm', models.FloatField(blank=True, null=True)),
                ('Carry_forword_Next_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeavePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Act', models.CharField(blank=True, choices=[('Factories Act', 'Factories Act'), ('Shops & Establishment Act', 'Shops & Establishment Act'), ('Custom', 'Custom')], max_length=30, null=True)),
                ('Type_of_leave', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('Eligibility_for_leave', models.IntegerField(blank=True, null=True)),
                ('No_of_leaves_pa', models.IntegerField(blank=True, null=True)),
                ('Leave_Encashment_pm', models.FloatField(blank=True, null=True)),
                ('Carry_forword_Next_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopEstablishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type_of_leave', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('Eligibility_for_leave', models.IntegerField(blank=True, null=True)),
                ('No_of_leaves_pa', models.IntegerField(blank=True, null=True)),
                ('Leave_Encashment_pm', models.FloatField(blank=True, null=True)),
                ('Carry_forword_Next_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SwipeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(blank=True, null=True)),
                ('Year', models.CharField(blank=True, max_length=4, null=True)),
                ('Month', models.CharField(blank=True, max_length=10, null=True)),
                ('SwipeIN', models.TimeField(blank=True, null=True)),
                ('SwipeOut', models.TimeField(blank=True, null=True)),
                ('SwipeHours', models.CharField(blank=True, max_length=20, null=True)),
                ('Shifts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Attendence.employeeshifts')),
                ('emp_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employee.employee_info')),
            ],
        ),
        migrations.CreateModel(
            name='Leavetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(blank=True, max_length=20, null=True)),
                ('year', models.CharField(blank=True, max_length=20, null=True)),
                ('credit_leave', models.JSONField(blank=True, default=dict, null=True)),
                ('leave_utilised', models.JSONField(blank=True, default=dict, null=True)),
                ('closing_bal', models.JSONField(blank=True, default=dict, null=True)),
                ('emp_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employee.employee_info')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Year', models.CharField(blank=True, max_length=4, null=True)),
                ('Month', models.CharField(blank=True, max_length=10, null=True)),
                ('Days', models.JSONField(blank=True, default=dict, null=True)),
                ('No_of_WeekOffs', models.CharField(blank=True, max_length=3, null=True)),
                ('No_of_holidays', models.CharField(blank=True, max_length=3, null=True)),
                ('Working_days', models.CharField(blank=True, max_length=3, null=True)),
                ('Total_days', models.CharField(blank=True, max_length=3, null=True)),
                ('Days_present', models.CharField(blank=True, max_length=3, null=True)),
                ('Days_absent', models.CharField(blank=True, max_length=3, null=True)),
                ('Leaves_allowed', models.CharField(blank=True, max_length=3, null=True)),
                ('LOP_leaves', models.CharField(blank=True, max_length=3, null=True)),
                ('Net_payable_days', models.CharField(blank=True, max_length=3, null=True)),
                ('emp_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employee.employee_info')),
            ],
        ),
        migrations.CreateModel(
            name='ApplyLeaves',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Year', models.CharField(blank=True, max_length=4, null=True)),
                ('Start_date', models.DateField(blank=True, null=True)),
                ('End_date', models.DateField(blank=True, null=True)),
                ('No_of_days', models.IntegerField(blank=True, null=True)),
                ('applied_date', models.DateField(auto_now_add=True, null=True)),
                ('Reporting_Manager', models.CharField(blank=True, max_length=30, null=True)),
                ('Status', models.CharField(blank=True, choices=[('Approve', 'Approve'), ('Not Approve', 'Not Approve')], max_length=30, null=True)),
                ('Action_date', models.DateField(auto_now_add=True, null=True)),
                ('Action_by', models.CharField(blank=True, max_length=30, null=True)),
                ('remark', models.CharField(blank=True, max_length=30, null=True)),
                ('Type_of_leave', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Attendence.leavepolicy')),
                ('emp_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employee.employee_info')),
            ],
        ),
    ]
