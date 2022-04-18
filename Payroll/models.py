import math
from django.db import models
from InTax.models import Salary_Heads, PF_Empr, Esi_Ratecard, PT_Header, PT_Slab
from Global.models import Financial_Year, Cont_State
from Organisation.models import Organisation_Info
from Employee.models import Employee_Info
from Attendence.models import *
from functools import reduce
from .utils import str_fmt, SalaryHeads
from .constants import salsetup_cate, month, status_choices
from dateutil import relativedelta
from datetime import datetime,timedelta
import fiscalyear
import calendar
from fiscalyear import FiscalYear
fiscalyear.setup_fiscal_calendar(start_month=4)


# Create your models here.


class CoSalsetup(models.Model):
    """
    This class represents template name and employeer pf&esi details
    """
    temp_name = models.CharField(max_length=30, blank=True, null=True)
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    org_id = models.ForeignKey(Organisation_Info, on_delete=models.CASCADE, blank=True, null=True)
    cate = models.CharField(max_length=15, choices=salsetup_cate, blank=True, null=True)
    sub_cate = models.CharField(max_length=15, blank=True, null=True)
    pf = models.ForeignKey(PF_Empr, on_delete=models.CASCADE, blank=True, null=True)
    esi = models.ForeignKey(Esi_Ratecard, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.temp_name


class CompanySalsetup(models.Model):
    """
    This class represents Company salary definition
    """
    particulars = models.ForeignKey(Salary_Heads, on_delete=models.CASCADE, blank=True, null=True)
    co_salsetups = models.ForeignKey(CoSalsetup, on_delete=models.CASCADE, blank=True, null=True)
    percent = models.IntegerField(blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.particulars.desc


class EmpCtcMaster(models.Model):
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.CASCADE, blank=True, null=True, unique=True)
    temp = models.ForeignKey(CoSalsetup, on_delete=models.CASCADE, blank=True, null=True)
    ctc = models.IntegerField(blank=True, null=True)
    eff_date = models.DateField(blank=True, null=True)
    actc = models.IntegerField(blank=True, null=True)
    incr_date_1 = models.DateField(blank=True, null=True)
    incr_ctc_1 = models.IntegerField(blank=True, null=True)
    eff_date_1 = models.DateField(blank=True, null=True)
    incr_date_2 = models.DateField(blank=True, null=True)
    incr_ctc_2 = models.IntegerField(blank=True, null=True)
    eff_date_2 = models.DateField(blank=True, null=True)
    incr_date_3 = models.DateField(blank=True, null=True)
    incr_ctc_3 = models.IntegerField(blank=True, null=True)
    eff_date_3 = models.DateField(blank=True, null=True)
    incr_date_4 = models.DateField(blank=True, null=True)
    incr_ctc_4 = models.IntegerField(blank=True, null=True)
    eff_date_4 = models.DateField(blank=True, null=True)
    salary_head = models.JSONField(default=dict, blank=True, null=True)

    def sal_head_cala(self, col_sal):
        
        salary_head = {}
        basic = [i.percent for i in col_sal if "basic" in str_fmt(i.particulars.desc)][0]
        for salsetup in col_sal:
            if str_fmt(salsetup.type) == "ctc":
                salary_head[salsetup.particulars.desc] = (self.ctc * salsetup.percent) // 100
            elif str_fmt(salsetup.type) == "basic":
                salary_head[salsetup.particulars.desc] = (self.ctc * (basic / 100) * salsetup.percent) / 100
            else:
                salary_head[salsetup.particulars.desc] = salsetup.limit or 0

        sum_value = reduce((lambda x, y: x + y), salary_head.values())
        esi = self.temp.esi
        pf = self.temp.pf
        # employeer pf calculation
        if salary_head[SalaryHeads.basicsalary.value] > (pf.Basic*12) and str_fmt(pf.restricted) == "yes":
            pf_empr = (pf.Basic*12) * pf.rate / 100
        else:
            pf_empr = salary_head[SalaryHeads.basicsalary.value] * pf.rate / 100
        salary_head[SalaryHeads.otherallowance.value] =(math.ceil(self.ctc - pf_empr - (sum_value * (1 + esi.empr_rate))) // (1 + esi.empr_rate))
        gross_salary = sum_value + salary_head[SalaryHeads.otherallowance.value]
        # Employeer Esi Calculation
        if gross_salary <= esi.limit*12:
            esi_empr = round(gross_salary * esi.empr_rate)
        else:
            esi_empr = 0
            salary_head[SalaryHeads.otherallowance.value] = round(self.ctc - pf_empr - sum_value)
        return salary_head

    def ctcfun(self, *args, **kwargs):
        salary_heads = self.temp.companysalsetup_set.all()
        salary_head = self.sal_head_cala(salary_heads)
        d = datetime(self.fy.start.year, self.fy.start.month, self.fy.start.day)
        end = self.eff_date + relativedelta.relativedelta(day=31)
        days = (end.day - self.eff_date.day) + 1
        day = (end.day - days)
        b = [i for i in salary_head.keys()]
        h = [(math.ceil((i / 12) / end.day) * days) for i in salary_head.values()]
        k = [math.ceil((i / 12))for i in salary_head.values()]
        EmpMonthCtcMaster.objects.update_or_create(fy=self.fy, emp_code=self.emp_code, month=self.eff_date.strftime("%b"),
                                                   temp=self.temp, ctc=self.ctc//12, salary_head=dict(zip(b, k)))

        ##lastmonth = calendar.month_abbr[end.month - 1]
        try:
            if self.eff_date.day > 1:
                qq = [i.salary_head for i in EmpMonPayroll.objects.filter(emp_code=self.emp_code,
                                                            month=(end.replace(day=1) - timedelta(1)).strftime("%b"), fy=self.fy)][0]
                j = [math.ceil((i / end.day) * day) for i in qq.values()]
                h = [i+j for i, j in zip(j, h)]

            if self.eff_date.day <= end.day:
                EmpMonPayroll.objects.update_or_create(emp_code=self.emp_code, month=end.strftime("%b"),
                                            fy=self.fy, defaults={'salary_head': dict(zip(b, h))})

        except Exception as e:
            EmpMonPayroll.objects.create(emp_code=self.emp_code, month=end.strftime("%b"),fy=self.fy,
                                         salary_head=dict(zip(b, h)))

        for m in range(0, 12):
            next_month_start = d + relativedelta.relativedelta(months=m, day=1)
            try:
                if self.eff_date < next_month_start.date():
                    EmpMonPayroll.objects.update_or_create(emp_code=self.emp_code,
                            month=next_month_start.strftime("%b"), fy=self.fy, defaults={'salary_head': dict(zip(b, k))})

            except Exception as e:
                EmpMonPayroll.objects.create(emp_code=self.emp_code,
                            month=next_month_start.strftime("%b"), fy=self.fy, salary_head=dict(zip(b, k)))
        try:
            if self.emp_code.dor.day > 1:

                ends = self.emp_code.dor + relativedelta.relativedelta(day=31)
                rdays = ends.day - self.emp_code.dor.day
                wday = (ends.day - rdays)
                qq = [i.salary_head for i in EmpMonPayroll.objects.filter(emp_code=self.emp_code,
                                    month=(ends.replace(day=1) - timedelta(1)).strftime("%b"),fy=self.fy)][0]
                j = [math.ceil((i / ends.day) * wday) for i in qq.values()]
                EmpMonPayroll.objects.update_or_create(emp_code=self.emp_code, month=self.emp_code.dor.strftime("%b"),
                                                       fy=self.fy, defaults={'salary_head': dict(zip(b, j))})
        except Exception as e:
            EmpMonPayroll.objects.filter(emp_code=self.emp_code,
                        month=(ends.replace(day=1) + timedelta(1)).strftime("%b"), fy=self.fy, salary_head=dict(zip(b, k))).delete()

    def save(self, *args, **kwargs):
        salary_heads = self.temp.companysalsetup_set.all()
        self.salary_head = self.sal_head_cala(salary_heads)
        try:
            if self.emp_code.doj != None:
                 self.ctc = self.actc
                 self.eff_date = self.emp_code.doj
            else:
                pass
            if self.eff_date_1 > self.emp_code.doj:
                self.ctc = self.incr_ctc_1
                self.eff_date = self.eff_date_1
            else:
                pass
            if self.eff_date_2 > self.eff_date_1:
                self.ctc = self.incr_ctc_2
                self.eff_date = self.eff_date_2
            else:
                pass
            if self.eff_date_3 > self.eff_date_2:
                self.ctc = self.incr_ctc_3
                self.eff_date = self.eff_date_3
            else:
                pass
            if self.eff_date_4 > self.eff_date_3:
                self.ctc = self.incr_ctc_4
                self.eff_date = self.eff_date_4
            else:
                pass
        except Exception as e:
            print(e)
        super(EmpCtcMaster, self).save(*args, **kwargs)
        self.ctcfun()



class EmpMonthCtcMaster(models.Model):
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.CASCADE, blank=True, null=True)
    month = models.CharField(max_length=15, blank=True, null=True)
    temp = models.ForeignKey(CoSalsetup, on_delete=models.CASCADE, blank=True, null=True)
    ctc = models.IntegerField(blank=True, null=True)
    salary_head = models.JSONField(default=dict, blank=True, null=True)


class EmpMonPayroll(models.Model):
    """
    This class represents Employee monthly payroll Information
    """
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.CASCADE, blank=True, null=True)
    month = models.CharField(max_length=15, blank=True, null=True)
    salary_head = models.JSONField(default=dict, blank=True, null=True)
    pf = models.FloatField(blank=True, null=True)
    pt = models.FloatField(blank=True, null=True)
    esi = models.FloatField(blank=True, null=True)
    tds = models.FloatField(blank=True, null=True)
    pf_empr = models.FloatField(blank=True, null=True)
    esi_empr = models.FloatField(blank=True, null=True)
    gross_salary = models.FloatField(blank=True, null=True)
    net_salary = models.FloatField(blank=True, null=True)
    tax_income = models.JSONField(default=dict, blank=True, null=True)
    non_tax_income = models.JSONField(default=dict, blank=True, null=True)
    other_dedu = models.JSONField(default=dict, blank=True, null=True)
    Total_days = models.CharField(max_length=3, null=True, blank=True)
    LOP_leaves = models.CharField(max_length=3, null=True, blank=True)
    Net_payable_days = models.CharField(max_length=3, null=True, blank=True)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.gross_salary = reduce((lambda x, y: x + y), self.salary_head.values())
        esi = self.fy.esi_ratecard_set.get(fy=self.fy)
        pf = self.fy.pf_empr_set.get(fy=self.fy)
        emp_pf = self.fy.pf_emp_set.get(fy=self.fy)
    # Employeer Esi Calculation
        if self.gross_salary <= esi.limit:
            self.esi_empr = round(self.gross_salary * esi.empr_rate)
        else:
            self.esi_empr = 0
    # Employee Esi Calculation
        if self.gross_salary <= esi.limit:
            self.esi = round(self.gross_salary * esi.emp_rate)
        else:
            self.esi = 0
        # employeer pf calculation
        if self.salary_head[SalaryHeads.basicsalary.value] > pf.Basic and str_fmt(pf.restricted) == "yes":
            self.pf_empr = math.ceil(pf.Basic * pf.rate / 100)
        else:
            self.pf_empr = self.salary_head[SalaryHeads.basicsalary.value] * pf.rate / 100

        # emp pf calculations
        if self.salary_head[SalaryHeads.basicsalary.value] > emp_pf.Basic and str_fmt(emp_pf.restricted) == "yes":
            self.pf = math.ceil(emp_pf.Basic * emp_pf.rate / 100)
        else:
            self.pf = self.salary_head[SalaryHeads.basicsalary.value] * emp_pf.rate / 100
        # pt calculation
        for slabs in PT_Header.objects.filter(state=Cont_State.objects.get(state=self.emp_code.pres_addr.get('state'))):
            for rate in slabs.pt_slab_set.all():
                if self.gross_salary <= (rate.range_min or 0):
                    self.pt = rate.rate
                elif self.gross_salary >= (rate.range_min or 0) and self.gross_salary <= (rate.range_max or 0):
                    self.pt = rate.rate
                else:
                    self.pt = rate.rate
        leave = self.emp_code.attendancereport_set.get(emp_code=self.emp_code)

        if self.month == "Dec":
            self.LOP_leaves = leave.LOP_leaves
            self.Total_days = leave.Total_days
            self.Net_payable_days = leave.Net_payable_days


        super(EmpMonPayroll, self).save(*args, **kwargs)

class TaxDeclaration(models.Model):
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    org_id = models.ForeignKey(Organisation_Info, on_delete=models.CASCADE, blank=True, null=True)
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.CASCADE, blank=True, null=True)
    Template_name = models.CharField(max_length=30, blank=True, null=True)
    emp_estimated = models.JSONField(default=dict, blank=True, null=True)
    estimated_status = models.CharField(max_length=20, null=True, blank=True, choices=status_choices)
    estimated_allowed = models.JSONField(default=dict, blank=True, null=True)
    allowed_status = models.CharField(max_length=20, null=True, blank=True, choices=status_choices)
    emp_actual_amount = models.JSONField(default=dict, blank=True, null=True)
    actual_amount_status = models.CharField(max_length=20, null=True, blank=True, choices=status_choices)
    actual_allowed = models.JSONField(default=dict, blank=True, null=True)
    actual_allowed_status = models.CharField(max_length=20, null=True, blank=True, choices=status_choices)
    remarks = models.CharField(max_length=20, null=True, blank=True)

class TaxDeclarationAtt(models.Model):
    tax_decl = models.ForeignKey(TaxDeclaration, on_delete=models.CASCADE, blank=True, null=True)
    attachments = models.FileField(null=True, blank=True)

