from django.db import models
from .constants import conditions, taxcategory, tax_type, pf_cate, rest_choice, Regime
from Global.models import Timestamps, Cont_State, Financial_Year

# Create your models here.

class Tax_header(Timestamps, models.Model):
    """
    This class represents Income tax header details
    """
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=20, choices=tax_type, blank=True, null=True)
    cate = models.CharField(max_length=20, choices=taxcategory, blank=True, null=True)
    age_min = models.IntegerField(blank=True, null=True)
    cdn_max = models.CharField(max_length=20, choices=conditions, blank=True, null=True)
    age_max = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.type


class Tax_slab(Timestamps, models.Model):
    """
    This class represents Income tax slab details
    """
    slab = models.ForeignKey(Tax_header, on_delete=models.CASCADE, blank=True, null=True)
    rang_min = models.IntegerField(blank=True, null=True)
    cdn_max = models.CharField(max_length=20, choices=conditions, blank=True, null=True)
    rang_max = models.IntegerField(blank=True, null=True)
    tax_rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.slab.cate
    
    
class PT_Header(Timestamps, models.Model):
    """
    This class represents PT Header details
    """
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(Cont_State, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.state.state


class PT_Slab(Timestamps, models.Model):
    """
    This class represents PT Slab details
    """
    state = models.ForeignKey(PT_Header, on_delete=models.CASCADE, blank=True)
    range_min = models.IntegerField(blank=True, null=True)
    cdn_max = models.CharField(max_length=20, choices=conditions, blank=True, null=True)
    range_max = models.IntegerField(blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True)
    slab = models.IntegerField(blank=True, null=True)
    
    
class PF_Empr(Timestamps, models.Model):
    """
    This class represents Employeer pf rates and details
    """
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    cate = models.CharField(max_length=20, choices=pf_cate, blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True)
    restricted = models.CharField(max_length=5, choices=rest_choice, blank=True)
    Basic = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.cate


class PF_Emp(Timestamps, models.Model):
    """
    This class represents Employee pf rates and details
    """
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    cate = models.CharField(max_length=20, blank=True, choices=pf_cate, null=True)
    rate = models.IntegerField(blank=True, null=True)
    restricted = models.CharField(max_length=5, choices=rest_choice, blank=True)
    Basic = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.cate
    
    
class Esi_Ratecard(Timestamps, models.Model):
    """
    This class represents Esi details
    """
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    empr_rate = models.FloatField(blank=True, null=True)
    emp_rate = models.FloatField(blank=True, null=True)
    block1_from = models.DateField(blank=True, null=True)
    block1_to = models.DateField(blank=True, null=True)
    block2_from = models.DateField(blank=True, null=True)
    block2_to = models.DateField(blank=True, null=True)

    def __int__(self):
        return self.fy
    
    
class Salary_Heads(Timestamps, models.Model):
    """
    This class represents salary heads
    """
    sec_no = models.CharField(max_length=20, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    editable = models.BooleanField(default=False)

    def __str__(self):
        return self.desc
    
    
class Exemptions(Timestamps, models.Model):
    """
    This class represents Exemptions Conditions details
    """
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    regime = models.CharField(max_length=20, choices=Regime, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    sec = models.CharField(max_length=10, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    ref_earn = models.ForeignKey(Salary_Heads, on_delete=models.CASCADE, blank=True, null=True)
    ceil_pm = models.IntegerField(blank=True, null=True)
    ceil_pa = models.IntegerField(blank=True, null=True)
    hra_mc = models.FloatField(blank=True, null=True)
    hra_nmc = models.FloatField(blank=True, null=True)
    sal_per = models.FloatField(blank=True, null=True)  # % of sal used for hra  exemp cal
    avg_hlfsal = models.FloatField(blank=True, null=True)  # half mon sal used for gratuity retairement compensation
    months = models.IntegerField(blank=True, null=True)
    leave_division = models.FloatField(blank=True, null=True)
    avg_monsal = models.IntegerField(blank=True, null=True)  # average months sal
    commuted_pension = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.desc
    
    
class Chp_VIA_Deductions(Timestamps, models.Model):
    """
    This class represents Chapter VI A Conditions details
    """
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    regime = models.CharField(max_length=20, choices=Regime, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    sec = models.CharField(max_length=10, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    ceili_pm = models.IntegerField(blank=True, null=True)
    ceili_pa = models.IntegerField(blank=True, null=True)
    deduct_mx = models.FloatField(blank=True, null=True)
    sal_per = models.FloatField(blank=True, null=True)
    excess_gti = models.FloatField(blank=True, null=True)
    adj_gti = models.FloatField(blank=True, null=True)
    norm_disab = models.IntegerField(blank=True, null=True)
    severe_disab = models.IntegerField(blank=True, null=True)
    citizen = models.IntegerField(blank=True, null=True)
    sr_citizen = models.IntegerField(blank=True, null=True)
    loan_sancfrm = models.DateField(blank=True, null=True)
    loan_sancto = models.DateField(blank=True, null=True)
    sdv_property = models.IntegerField(blank=True, null=True)
    loan_amt = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.sec
    
    
class Sec16_Dedu(Timestamps, models.Model):
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    regime = models.CharField(max_length=20, choices=Regime, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    sec = models.CharField(max_length=10, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    ceil_limit = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.desc


class FactoriesAct(models.Model):
    Type_of_leave = models.CharField(max_length=30, null=True, blank=True, unique=True)
    Eligibility_for_leave = models.IntegerField(null=True, blank=True)
    No_of_leaves_pa = models.IntegerField(null=True, blank=True)
    Leave_Encashment_pm = models.FloatField(null=True, blank=True)
    Carry_forword_Next_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Type_of_leave


class ShopEstablishment(models.Model):
    Type_of_leave = models.CharField(max_length=30, null=True, blank=True, unique=True)
    Eligibility_for_leave = models.IntegerField(null=True, blank=True)
    No_of_leaves_pa = models.IntegerField(null=True, blank=True)
    Leave_Encashment_pm = models.FloatField(null=True, blank=True)
    Carry_forword_Next_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Type_of_leave
