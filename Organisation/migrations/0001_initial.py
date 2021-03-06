# Generated by Django 4.0.3 on 2022-04-05 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_code', models.CharField(max_length=20, unique=True)),
                ('org_name', models.CharField(max_length=255, null=True)),
                ('org_regno', models.BigIntegerField(blank=True, null=True)),
                ('doi', models.DateField(blank=True, null=True)),
                ('org_type', models.CharField(blank=True, choices=[('Govt', 'Govt'), ('Others', 'Others')], max_length=20, null=True)),
                ('buss_nature', models.CharField(blank=True, max_length=50, null=True)),
                ('ind_type', models.CharField(blank=True, max_length=50, null=True)),
                ('reg_offaddr', models.JSONField(default=dict)),
                ('website', models.URLField(blank=True, null=True)),
                ('pan', models.CharField(max_length=10, null=True, unique=True)),
                ('pan_circ', models.CharField(blank=True, max_length=50, null=True)),
                ('tan', models.CharField(max_length=20, unique=True)),
                ('tds_circ', models.CharField(blank=True, max_length=50, null=True)),
                ('gstin', models.CharField(max_length=50, unique=True)),
                ('gst_regdt', models.DateField(blank=True, null=True)),
                ('gst_circ', models.CharField(blank=True, max_length=50, null=True)),
                ('deductor_type', models.CharField(blank=True, choices=[('Govt', 'Govt'), ('Union Govt', 'Union Govt'), ('LLP', 'LLP'), ('Partnership Firm', 'Partnership Firm'), ('OPC', 'OPC'), ('Section-8 Company', 'Section-8 Company'), ('Pvt Ltd', 'Pvt.Ltd'), ('Public Ltd', 'Public.Ltd'), ('Others', 'Others')], max_length=20, null=True)),
                ('epf_code', models.CharField(blank=True, max_length=30, null=True)),
                ('pf_covgdt', models.DateField(blank=True, null=True)),
                ('pf_regdt', models.DateField(blank=True, null=True)),
                ('pf_regoffc', models.CharField(blank=True, max_length=30, null=True)),
                ('esi_regno', models.CharField(blank=True, max_length=20, null=True)),
                ('esi_regd', models.DateField(blank=True, null=True)),
                ('esi_covgdt', models.DateField(blank=True, null=True)),
                ('esi_locoffc', models.CharField(blank=True, max_length=50, null=True)),
                ('ptemp_regno', models.CharField(blank=True, max_length=20, null=True)),
                ('ptcomp_regno', models.CharField(blank=True, max_length=20, null=True)),
                ('pto_circ', models.CharField(blank=True, max_length=20, null=True)),
                ('pt_state', models.CharField(blank=True, max_length=30, null=True)),
                ('Corp_offcadr', models.JSONField(default=dict)),
                ('loc1_addr', models.JSONField(default=dict)),
                ('loc2_addr', models.JSONField(default=dict)),
                ('loc3_addr', models.JSONField(default=dict)),
                ('loc4_addr', models.JSONField(default=dict)),
                ('loc5_addr', models.JSONField(default=dict)),
                ('auth_signname', models.CharField(blank=True, max_length=50, null=True)),
                ('father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('desig', models.CharField(blank=True, max_length=50, null=True)),
                ('dept', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact', models.CharField(blank=True, max_length=15, null=True)),
                ('auth_pan', models.CharField(blank=True, max_length=15, null=True)),
                ('auth_personname', models.CharField(blank=True, max_length=50, null=True)),
                ('auth_contact', models.CharField(blank=True, max_length=15, null=True)),
                ('auth_email', models.CharField(blank=True, max_length=50, null=True)),
                ('auth_dep', models.CharField(blank=True, max_length=50, null=True)),
                ('bank1_name', models.CharField(blank=True, max_length=50, null=True)),
                ('branch1_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank1_ifsc', models.CharField(blank=True, max_length=10, null=True)),
                ('acc1_no', models.BigIntegerField(blank=True, null=True)),
                ('acc1_type', models.CharField(blank=True, max_length=20, null=True)),
                ('bank2_name', models.CharField(blank=True, max_length=50, null=True)),
                ('branch2_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank2_ifsc', models.CharField(blank=True, max_length=10, null=True)),
                ('acc2_no', models.BigIntegerField(blank=True, null=True)),
                ('acc2_type', models.CharField(blank=True, max_length=20, null=True)),
                ('bank3_name', models.CharField(blank=True, max_length=50, null=True)),
                ('branch3_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank3_ifsc', models.CharField(blank=True, max_length=10, null=True)),
                ('acc3_no', models.BigIntegerField(blank=True, null=True)),
                ('acc3_type', models.CharField(blank=True, max_length=20, null=True)),
                ('bank4_name', models.CharField(blank=True, max_length=50, null=True)),
                ('branch4_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank4_ifsc', models.CharField(blank=True, max_length=10, null=True)),
                ('acc4_no', models.BigIntegerField(blank=True, null=True)),
                ('acc4_type', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desig_name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('org_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Organisation.organisation_info')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(blank=True, max_length=50, unique=True)),
                ('org_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Organisation.organisation_info')),
            ],
        ),
    ]
