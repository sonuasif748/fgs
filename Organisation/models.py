from django.db import models
from django.db.models import JSONField
from .constants import *
from Global.models import Timestamps

# Create your models here.

class Organisation_Info(models.Model):
    org_code = models.CharField(max_length=20, unique=True)
    org_name = models.CharField(max_length=255, null=True)
    org_regno = models.BigIntegerField(blank=True, null=True)
    doi = models.DateField(blank=True, null=True) #date of incorporation
    org_type = models.CharField(max_length=20, choices=type_of_company, blank=True, null=True)
    buss_nature = models.CharField(max_length=50, blank=True, null=True)
    ind_type = models.CharField(max_length=50, blank=True, null=True)
    reg_offaddr = JSONField(default=dict)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    pan = models.CharField(max_length=10, unique=True, null=True)
    pan_circ = models.CharField(max_length=50, blank=True, null=True)
    tan = models.CharField(max_length=20, unique=True)
    tds_circ = models.CharField(max_length=50, blank=True, null=True)
    gstin = models.CharField(max_length=50, unique=True)
    gst_regdt = models.DateField(blank=True, null=True)
    gst_circ = models.CharField(max_length=50, blank=True, null=True)
    deductor_type = models.CharField(max_length=20, choices=deductor, blank=True, null=True) 
    epf_code = models.CharField(max_length=30, blank=True, null=True)
    pf_covgdt = models.DateField(blank=True, null=True)
    pf_regdt = models.DateField(blank=True, null=True)
    pf_regoffc = models.CharField(max_length=30, blank=True, null=True)
    esi_regno = models.CharField(max_length=20, blank=True, null=True)
    esi_regd = models.DateField(blank=True, null=True)
    esi_covgdt = models.DateField(blank=True, null=True)
    esi_locoffc = models.CharField(max_length=50, blank=True, null=True)
    ptemp_regno = models.CharField(max_length=20, blank=True, null=True)
    ptcomp_regno = models.CharField(max_length=20, blank=True, null=True)
    pto_circ = models.CharField(max_length=20, blank=True, null=True)
    pt_state = models.CharField(max_length=30, blank=True, null=True)
    Corp_offcadr = JSONField(default=dict)
    loc1_addr = JSONField(default=dict)
    loc2_addr = JSONField(default=dict)
    loc3_addr = JSONField(default=dict)
    loc4_addr = JSONField(default=dict)
    loc5_addr = JSONField(default=dict)
    auth_signname = models.CharField(max_length=50, blank=True, null=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    desig = models.CharField(max_length=50, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    auth_pan = models.CharField(max_length=15, blank=True, null=True)
    auth_personname = models.CharField(max_length=50, blank=True, null=True)
    auth_contact = models.CharField(max_length=15, blank=True, null=True)
    auth_email = models.CharField(max_length=50, blank=True, null=True)
    auth_dep = models.CharField(max_length=50, blank=True, null=True)
    bank1_name = models.CharField(max_length=50, blank=True, null=True)
    branch1_name = models.CharField(max_length=50, blank=True, null=True)
    bank1_ifsc = models.CharField(max_length=10, blank=True, null=True)
    acc1_no = models.BigIntegerField(blank=True, null=True)
    acc1_type = models.CharField(max_length=20, blank=True, null=True)
    bank2_name = models.CharField(max_length=50, blank=True, null=True)
    branch2_name = models.CharField(max_length=50, blank=True, null=True)
    bank2_ifsc = models.CharField(max_length=10, blank=True, null=True)
    acc2_no = models.BigIntegerField(blank=True, null=True)
    acc2_type = models.CharField(max_length=20, blank=True, null=True)
    bank3_name = models.CharField(max_length=50, blank=True, null=True)
    branch3_name = models.CharField(max_length=50, blank=True, null=True)
    bank3_ifsc = models.CharField(max_length=10, blank=True, null=True)
    acc3_no = models.BigIntegerField(blank=True, null=True)
    acc3_type = models.CharField(max_length=20, blank=True, null=True)
    bank4_name = models.CharField(max_length=50, blank=True, null=True)
    branch4_name = models.CharField(max_length=50, blank=True, null=True)
    bank4_ifsc = models.CharField(max_length=10, blank=True, null=True)
    acc4_no = models.BigIntegerField(blank=True, null=True)
    acc4_type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.org_code


class Department(Timestamps, models.Model):
    """
    This class represents Department details
    """
    org_id = models.ForeignKey(Organisation_Info, on_delete=models.CASCADE, blank=True, null=True)
    dept_name = models.CharField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.dept_name


class Designation(Timestamps, models.Model):
    """
    This class represents Designation details
    """
    org_id = models.ForeignKey(Organisation_Info, on_delete=models.CASCADE, blank=True, null=True)
    desig_name = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.desig_name
    
class Holidays(models.Model):
    fy = models.CharField(max_length=20, blank=True, null=True)
    org_id = models.ForeignKey(Organisation_Info, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    day = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name