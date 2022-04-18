import calendar
from datetime import date
def AddDictionary(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = (value + dict_1[key])
   return dict_3

def SubDictionary(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = (dict_1[key] - value)
   return dict_3

def createatt(self):
    from .models import EmployeeShifts, AttendanceReport
    from Organisation.models import Holidays
    import calendar
    holidays = [i for i in Holidays.objects.all()]
    Shifts = [i for i in EmployeeShifts.objects.all()]
    todaydate = date.today().day
    b = calendar.monthlen(self.End_date.year, self.End_date.month)
    cal = calendar.monthcalendar(self.End_date.year, self.End_date.month)
    # cal = calendar.monthcalendar(self.End_date.year, self.End_date.month)
    key = [f'Date_{i}' for i in range(1, b + 1)]
    value = ['Absent' for i in range(1, b + 1)]
    mydict = {}
    for k, v in zip(key, value):
        mydict.update({k: v})
    for i in holidays:
        if i.date.month == self.End_date.month:
            mydict[f'Date_{i.date.day}'] = 'Holiday'
    for i in Shifts:
        if i.emp_code == self.emp_code:
            a = [cal[m][int(i.weekoffs[0])] for m in range(0, 5) or range(0, 6) if cal[m][int(i.weekoffs[0])] != 0]
            if len(i.weekoffs) > 1:
                a += [cal[m][int(i.weekoffs[1])] for m in range(0, 5) or range(0, 6) if cal[m][int(i.weekoffs[1])] != 0]
            else:
                pass
            for k in a:
                mydict[f'Date_{k}'] = 'Weekoff'
    obj, create = AttendanceReport.objects.update_or_create(emp_code=self.emp_code, Year=self.Year, Month=self.End_date.month,
                                                            defaults={'Days': mydict})

def createattinswipe(self):
    from .models import EmployeeShifts, AttendanceReport
    from Employee.models import Employee_Info
    from Organisation.models import Holidays
    import calendar
    import fiscalyear
    from fiscalyear import FiscalYear, FiscalMonth
    fiscalyear.setup_fiscal_calendar(start_month=1)
    for j in Employee_Info.objects.all():
        holidays = [i for i in Holidays.objects.all()]
        Shifts = [i for i in EmployeeShifts.objects.all()]
        todaydate = date.today().day
        b = FiscalMonth(date.today().year, date.today().month).end.day

        cal = calendar.monthcalendar(date.today().year, date.today().month)
        key = [f'Date_{i}' for i in range(1, b + 1)]
        value = ['Absent' for i in range(1, b + 1)]
        mydict = {}
        for k, v in zip(key, value):
            mydict.update({k: v})
        for i in holidays:
            if i.date.month == date.today().month:
                mydict[f'Date_{i.date.day}'] = 'Holiday'
        for i in Shifts:
            if i.emp_code == j:
                a = [cal[m][int(i.weekoffs[0])] for m in range(0, 5) or range(0, 6) if
                     cal[m][int(i.weekoffs[0])] != 0]
                if len(i.weekoffs) > 1:
                    a += [cal[m][int(i.weekoffs[1])] for m in range(0, 5) or range(0, 6) if
                          cal[m][int(i.weekoffs[1])] != 0]
                else:
                    pass
                for k in a:
                    mydict[f'Date_{k}'] = 'Weekoff'
        obj, create = AttendanceReport.objects.update_or_create(emp_code=j, Year=self.Year, Month=self.Month,
                                                                defaults={'Days': mydict})