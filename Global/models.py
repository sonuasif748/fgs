from django.db import models
import fiscalyear
from dateutil import relativedelta
from fiscalyear import FiscalYear
fiscalyear.setup_fiscal_calendar(start_month=4)

# Create your models here.

class Timestamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
        
        
class Financial_Year(models.Model):
    """
    This class represents Financial Year
    """
    year = models.IntegerField(blank=True, null=True)
    fy_yr = models.CharField(max_length=10, blank=True, null=True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    q1_from = models.DateField(blank=True, null=True)
    q1_to = models.DateField(blank=True, null=True)
    q2_from = models.DateField(blank=True, null=True)
    q2_to = models.DateField(blank=True, null=True)
    q3_from = models.DateField(blank=True, null=True)
    q3_to = models.DateField(blank=True, null=True)
    q4_from = models.DateField(blank=True, null=True)
    q4_to = models.DateField(blank=True, null=True)
    h1_from = models.DateField(blank=True, null=True)
    h1_to = models.DateField(blank=True, null=True)
    h2_from = models.DateField(blank=True, null=True)
    h2_to = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.fy_yr

    def save(self, *args, **kwargs):
        yr = FiscalYear(self.year)
        self.fy_yr = str(yr.start.year) + "-" + str(yr.end.year)
        self.start = yr.start.date()
        self.end = yr.end.date()
        self.q1_from = yr.q1.start.date()
        self.q1_to = yr.q1.end.date()
        self.q2_from = yr.q2.start.date()
        self.q2_to = yr.q2.end.date()
        self.q3_from = yr.q3.start.date()
        self.q3_to = yr.q3.end.date()
        self.q4_from = yr.q4.start.date()
        self.q4_to = yr.q4.end.date()
        self.h1_from = yr.q1.start.date()
        self.h1_to = yr.q2.end.date()
        self.h2_from = yr.q3.start.date()
        self.h2_to = yr.q4.end.date()
        super(Financial_Year, self).save(*args, **kwargs)


class Country(models.Model):
    """
    This class represents Country Details
    """
    country = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.country


class Cont_State(models.Model):
    """
    This class represents Country with state Details
    """
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.state