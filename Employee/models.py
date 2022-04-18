from django.db import models
from django.db.models import JSONField
from .constants import *
from Organisation.models import Organisation_Info, Department, Designation
from datetime import datetime
# Create your models here.

class Employee_Info(models.Model):
    """ 
    This class represents Employee details
    """
    org_id = models.ForeignKey(Organisation_Info, on_delete=models.CASCADE, blank=True, null=True)
    emp_code = models.CharField(max_length=20, null=True, unique=True)
    emp_name = JSONField(default=dict, null=True, blank=True)
    emp_aadharname = models.CharField(max_length=50, null=True, blank=True)
    spouse_name = JSONField(default=dict, null=True,blank=True)
    gndr = models.CharField(max_length=10, choices=Genders, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    perm_addr = JSONField(default=dict)
    pres_addr = JSONField(default=dict)
    loc = models.CharField(max_length=20, blank=True, null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    desig = models.ForeignKey(Designation, on_delete=models.CASCADE, blank=True, null=True)
    doj = models.DateField(blank=True, null=True, unique=True)
    probation = models.CharField(max_length=10, blank=True, null=True)
    notice_period = models.CharField(max_length=10, blank=True, null=True)
    dor = models.DateField(blank=True, null=True)
    resig_resns = models.TextField(max_length=255, blank=True, null=True)
    email = JSONField(default=dict)
    contact = JSONField(default=dict, null=True, blank=True)
    bld_grp = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=20, blank=True, null=True)
    dependents = models.JSONField(default=dict)
    maritial_status = models.CharField(max_length=20, choices=maritial_status, blank=True, null=True)
    dom = models.DateField(blank=True, null=True)
    pan = models.CharField(max_length=10, blank=True, null=True, unique=True)
    adaar_no = models.BigIntegerField(blank=True, null=True)
    edu_qual = models.CharField(max_length=20, choices=qualifications, blank=True, null=True)
    emerg_cont1 = JSONField(default=dict)
    emerg_cont2 = JSONField(default=dict)
    nominee_dtl = JSONField(default=dict)
    bnk_name = models.CharField(max_length=50, blank=True, null=True)
    brch_name = models.CharField(max_length=50, blank=True, null=True)
    bank_ifsc = models.CharField(max_length=10, blank=True, null=True)
    acc_no = models.BigIntegerField(blank=True, null=True)
    acc_type = models.CharField(max_length=20, blank=True, null=True)
    esi_appldt = models.DateField(blank=True, null=True) # esi_applicable_date
    esi_no = models.CharField(max_length=20, blank=True, null=True)
    pension_appli = models.CharField(max_length=10, choices=choices, blank=True, null=True)
    esi_joindt = models.DateField(blank=True, null=True)
    pf_appli = models.CharField(max_length=10, choices=choices, blank=True, null=True)
    phy_hdcap = models.CharField(max_length=10, choices=choices, blank=True, null=True)
    pf_cate = models.CharField(max_length=50, choices=pf_category, blank=True, null=True)
    prev_pfno = models.CharField(max_length=10, choices=choices, blank=True, null=True)
    pre_pfno = models.CharField(max_length=20, blank=True, null=True)
    pf_jod = models.DateField(blank=True, null=True)
    uan = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.emp_code


