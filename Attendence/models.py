from django.db import models
from .constants import *
from Employee.models import Employee_Info
from Global.models import Financial_Year
from InTax.models import *
from django.db.models import JSONField
from multiselectfield import MultiSelectField
from .utils import *
import fiscalyear
from fiscalyear import FiscalYear, FiscalMonth
fiscalyear.setup_fiscal_calendar(start_month=1)
from datetime import date, timedelta
# Create your models here.
import calendar


class Custom(models.Model):
    Type_of_leave = models.CharField(max_length=30, null=True, blank=True, unique=True)
    Eligibility_for_leave = models.IntegerField(null=True, blank=True)
    No_of_leaves_pa = models.IntegerField(null=True, blank=True)
    Leave_Encashment_pm = models.FloatField(null=True, blank=True)
    Carry_forword_Next_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Type_of_leave


class LeavePolicy(models.Model):
    fy = models.ForeignKey(Financial_Year, on_delete=models.CASCADE, blank=True, null=True)
    Act = models.CharField(max_length=30, null=True, blank=True, choices=Act_choice)
    Type_of_leave = models.CharField(max_length=30, null=True, blank=True, unique=True)
    Eligibility_for_leave = models.IntegerField(null=True, blank=True)
    No_of_leaves_pa = models.IntegerField(null=True, blank=True)
    Leave_Encashment_pm = models.FloatField(null=True, blank=True)
    Carry_forword_Next_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Type_of_leave


class ApplyLeaves(models.Model):
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.SET_NULL, blank=True, null=True)
    Type_of_leave = models.ForeignKey(LeavePolicy, on_delete=models.SET_NULL, blank=True, null=True)
    Year = models.CharField(max_length=4, null=True, blank=True)
    Start_date = models.DateField(null=True, blank=True)
    End_date = models.DateField(null=True, blank=True)
    No_of_days = models.IntegerField(null=True, blank=True)
    applied_date = models.DateField(null=True, blank=True, auto_now_add=True)
    Reporting_Manager = models.CharField(max_length=30, null=True, blank=True)
    Status = models.CharField(max_length=30, null=True, blank=True, choices=leave_status)
    Action_date = models.DateField(null=True, blank=True, auto_now_add=True)
    Action_by = models.CharField(max_length=30, null=True, blank=True)
    remark = models.CharField(max_length=30, null=True, blank=True)

    def leavetableupdate(self):
        typeofleave = self.Type_of_leave.Type_of_leave
        leave = [i for i in Leavetable.objects.filter(emp_code=self.emp_code, year=self.Year, month=self.Start_date.month)]
        leave_utilised = leave[0].leave_utilised
        credit_leave = leave[0].credit_leave
        if typeofleave in leave_utilised.keys():
            if self.Status == 'Approve':
                if self.Start_date.month == self.End_date.month:
                    data = [i.Days for i in AttendanceReport.objects.filter(emp_code=self.emp_code, Year=self.Year,
                                                                            Month=self.Start_date.month)]
                    leavedays = data[0]
                    day = [(self.Start_date + timedelta(days=i)).day for i in
                           range((self.End_date - self.Start_date).days + 1)]
                    for days in day:
                        leavedays[f'Date_{days}'] = 'Leave'
                    obj, create = AttendanceReport.objects.update_or_create(emp_code=self.emp_code, Year=self.Year,
                                                                            Month=self.Start_date.month,
                                                                            defaults={'Days': leavedays})
                    leave_utilised[typeofleave] = leave_utilised[typeofleave] + self.No_of_days
                    if self.Type_of_leave.Type_of_leave in ['Maternity Leave (ML)', 'Marriage Leave', 'Paternity Leave',
                                                            'Bereavement Leave']:
                        credit_leave[typeofleave] = self.No_of_days
                        obj, create = Leavetable.objects.update_or_create(emp_code=self.emp_code, year=self.Year,
                                                                          month=self.Start_date.month,
                                                                          defaults={'leave_utilised': leave_utilised,
                                                                                    'credit_leave': credit_leave}, )
                    obj, create = Leavetable.objects.update_or_create(emp_code=self.emp_code, year=self.Year,
                                                                      month=self.Start_date.month,
                                                                      defaults={'leave_utilised': leave_utilised}, )
                if self.Start_date.month != self.End_date.month:
                    leaves = (FiscalMonth(self.Start_date.year, self.Start_date.month).end.day) - (
                        self.Start_date.day) + 1
                    leave_utilised[typeofleave] = leave_utilised[typeofleave] + leaves
                    credit_leave[typeofleave] = credit_leave[typeofleave] + leaves
                    data = [i.Days for i in AttendanceReport.objects.filter(emp_code=self.emp_code, Year=self.Year,
                                                                            Month=self.Start_date.month)]
                    leavedays = data[0]
                    day = [(self.Start_date + timedelta(days=i)).day for i in range(leaves)]
                    for days in day:
                        leavedays[f'Date_{days}'] = 'Leave'
                    obj, create = AttendanceReport.objects.update_or_create(emp_code=self.emp_code, Year=self.Year,
                                                                            Month=self.Start_date.month,
                                                                            defaults={'Days': leavedays})
                    createatt(self)
                    data = [i.Days for i in AttendanceReport.objects.filter(emp_code=self.emp_code, Year=self.Year,
                                                                            Month=self.End_date.month)]
                    leavedays = data[0]
                    day = [i for i in range(self.End_date.day)]
                    for days in day:
                        leavedays[f'Date_{days}'] = 'Leave'
                    obj, create = AttendanceReport.objects.update_or_create(emp_code=self.emp_code, Year=self.Year,
                                                                            Month=self.End_date.month,
                                                                            defaults={'Days': leavedays})
                    if self.Type_of_leave.Type_of_leave in ['Maternity Leave (ML)', 'Marriage Leave', 'Paternity Leave',
                                                            'Bereavement Leave']:
                        obj, create = Leavetable.objects.update_or_create(emp_code=self.emp_code, year=self.Year,
                                                                          month=self.Start_date.month,
                                                                          defaults={'leave_utilised': leave_utilised,
                                                                                    'credit_leave': credit_leave}, )
                    obj, create = Leavetable.objects.update_or_create(emp_code=self.emp_code, year=self.Year,
                                                                      month=self.Start_date.month,
                                                                      defaults={'leave_utilised': leave_utilised}, )
                    leaves = self.End_date.day
                    leave_utilised[typeofleave] = leaves
                    credit_leave[typeofleave] = leaves
                    if self.Type_of_leave.Type_of_leave in ['Maternity Leave (ML)', 'Marriage Leave', 'Paternity Leave',
                                                            'Bereavement Leave']:
                        obj, create = Leavetable.objects.update_or_create(emp_code=self.emp_code, year=self.Year,
                                                                          month=self.End_date.month,
                                                                          defaults={'leave_utilised': leave_utilised,
                                                                                    'credit_leave': credit_leave}, )
                    obj, create = Leavetable.objects.update_or_create(emp_code=self.emp_code, year=self.Year,
                                                                      month=self.End_date.month,
                                                                      defaults={'leave_utilised': leave_utilised}, )

    def save(self, *args, **kwargs):
        self.No_of_days = (self.End_date - self.Start_date).days + 1
        super(ApplyLeaves, self).save(*args, **kwargs)
        self.leavetableupdate()


class Leavetable(models.Model):
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.SET_NULL, null=True, blank=True)
    month = models.CharField(max_length=20, null=True, blank=True)
    year = models.CharField(max_length=20, null=True, blank=True)
    credit_leave = JSONField(default=dict, null=True, blank=True)
    leave_utilised = JSONField(default=dict, null=True, blank=True)
    closing_bal = JSONField(default=dict, null=True, blank=True)

    def save(self, *args, **kwargs):
        opening_bal = {'Privilege Leave (PL)': 0, 'Casual Leave (CL)': 0, 'Sick Leave (SL)': 0,
                       'Maternity Leave (ML)': 0,
                       'Marriage Leave': 0, 'Paternity Leave': 0, 'Bereavement Leave': 0}
        self.closing_bal = SubDictionary(AddDictionary(opening_bal, self.credit_leave), self.leave_utilised)
        super(Leavetable, self).save(*args, **kwargs)


class EmployeeShifts(models.Model):
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.SET_NULL, blank=True, null=True)
    Year = models.CharField(max_length=4, null=True, blank=True)
    Month = models.CharField(max_length=10, null=True, blank=True)
    shift_name = models.CharField(max_length=50, blank=True, null=True)
    min_start_time = models.TimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    max_start_time = models.TimeField(blank=True, null=True)
    min_end_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    max_end_time = models.TimeField(blank=True, null=True)
    break_time = models.TimeField(blank=True, null=True)
    working_days = models.CharField(max_length=50, blank=True, null=True)
    shift_start = models.DateField(blank=True, null=True)
    shift_end = models.DateField(blank=True, null=True)
    weekoffs = MultiSelectField(max_length=30, null=True, blank=True, choices=weekoffschoices)
    indefnite = models.BooleanField(default=False)
    year_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.shift_name


class SwipeData(models.Model):
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.SET_NULL, blank=True, null=True)
    Shifts = models.ForeignKey(EmployeeShifts, on_delete=models.SET_NULL, blank=True, null=True)
    Date = models.DateField(blank=True, null=True)
    Year = models.CharField(max_length=4, null=True, blank=True)
    Month = models.CharField(max_length=10, null=True, blank=True)
    SwipeIN = models.TimeField(blank=True, null=True)
    SwipeOut = models.TimeField(blank=True, null=True)
    SwipeHours = models.CharField(max_length=20, blank=True, null=True)

    def createattendance(self):
        data = [i.Days for i in
                AttendanceReport.objects.filter(emp_code=self.emp_code, Year=self.Year, Month=self.Month)]
        if data == []:
            createattinswipe(self)
        data = [i.Days for i in
                AttendanceReport.objects.filter(emp_code=self.emp_code, Year=self.Year, Month=self.Month)]
        mydict = data[0]
        mydict[f'Date_{self.Date.day}'] = 'Present'
        obj, create = AttendanceReport.objects.update_or_create(emp_code=self.emp_code, Year=self.Year,
                                                                Month=self.Month,
                                                                defaults={'Days': mydict})

    def save(self, *args, **kwargs):
        self.SwipeHours = (self.SwipeOut.hour) - (self.SwipeIN.hour)
        super(SwipeData, self).save(*args, **kwargs)
        self.createattendance()


class AttendanceReport(models.Model):
    emp_code = models.ForeignKey(Employee_Info, on_delete=models.SET_NULL, blank=True, null=True)
    Year = models.CharField(max_length=4, null=True, blank=True)
    Month = models.CharField(max_length=10, null=True, blank=True)
    Days = JSONField(default=dict, null=True, blank=True)
    No_of_WeekOffs = models.CharField(max_length=3, null=True, blank=True)
    No_of_holidays = models.CharField(max_length=3, null=True, blank=True)
    Working_days = models.CharField(max_length=3, null=True, blank=True)
    Total_days = models.CharField(max_length=3, null=True, blank=True)
    Days_present = models.CharField(max_length=3, null=True, blank=True)
    Days_absent = models.CharField(max_length=3, null=True, blank=True)
    Leaves_allowed = models.CharField(max_length=3, null=True, blank=True)
    LOP_leaves = models.CharField(max_length=3, null=True, blank=True)
    Net_payable_days = models.CharField(max_length=3, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.No_of_holidays = sum('Holiday' in  subList for subList in self.Days.values())
        self.No_of_WeekOffs = sum('Weekoff' in  subList for subList in self.Days.values())
        self.Days_absent = sum('Absent' in  subList for subList in self.Days.values())
        self.Days_present = sum('Presents' in  subList for subList in self.Days.values())
        self.Leaves_allowed = sum('Leave' in  subList for subList in self.Days.values())
        self.Total_days = len(self.Days)
        self.Working_days = self.Total_days - self.No_of_WeekOffs - self.No_of_holidays
        self.LOP_leaves = self.Days_absent
        self.Net_payable_days = self.Total_days - self.LOP_leaves
        super(AttendanceReport, self).save(*args, **kwargs)

        # sum('Absent' in  subList for subList in self.Days.values())