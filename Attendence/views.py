from datetime import date, datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from Employee.models import Employee_Info
from .serializers import *
import fiscalyear
from fiscalyear import FiscalYear, FiscalMonth
fiscalyear.setup_fiscal_calendar(start_month=1)
from .utils import *



class Leavetableviews(APIView):
    def get(self, request):
        Employeedata = Employee_Info.objects.all()
        Leavepolicy = LeavePolicy.objects.all()
        lp = [i for i in Leavepolicy]
        applyleaves = ApplyLeaves.objects.all()
        for i in Employeedata:
            el = (0, 18 / 12)[(date.today() - i.doj).days >= 240 and i.dor == None]
            pl = (0, lp[0].No_of_leaves_pa / 12)[
                (date.today() - i.doj).days >= lp[0].Eligibility_for_leave and i.dor == None]
            cl = (0, lp[5].No_of_leaves_pa / 12)[
                (date.today() - i.doj).days >= lp[5].Eligibility_for_leave and i.dor == None]
            sl = (0, lp[6].No_of_leaves_pa / 12)[
                (date.today() - i.doj).days >= lp[6].Eligibility_for_leave and i.dor == None]
            close_open = [i for i in Leavetable.objects.filter(emp_code=i, month=date.today().month - 1)]
            if close_open == []:
                opening_bal = {'Privilege Leave (PL)': 0, 'Casual Leave (CL)': 0, 'Sick Leave (SL)': 0,
                               'Maternity Leave (ML)': 0,
                               'Marriage Leave': 0, 'Paternity Leave': 0, 'Bereavement Leave': 0}
            else:
                opening_bal = close_open[0].closing_bal
            credit_leave = {'Privilege Leave (PL)': pl, 'Casual Leave (CL)': cl, 'Sick Leave (SL)': sl,
                            'Maternity Leave (ML)': 0,
                            'Marriage Leave': 0, 'Paternity Leave': 0, 'Bereavement Leave': 0}
            leave_utilised = {'Privilege Leave (PL)': 0, 'Casual Leave (CL)': 0, 'Sick Leave (SL)': 0,
                              'Maternity Leave (ML)': 0,
                              'Marriage Leave': 0, 'Paternity Leave': 0, 'Bereavement Leave': 0}
            closing_bal = SubDictionary(AddDictionary(opening_bal, credit_leave), leave_utilised)
            Leavetable(emp_code=i, month=date.today().month, year=datetime.today().year,
                       credit_leave=credit_leave, leave_utilised=leave_utilised, closing_bal=closing_bal).save()
        return Response('done')


class ApplyLeave(APIView):
    def post(self, request):
        return Response('done')

class CustomList(generics.ListCreateAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerializer


class CustomDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerializer


class LeavePolicyList(generics.ListCreateAPIView):
    queryset = LeavePolicy.objects.all()
    serializer_class = LeavePolicySerializer


class LeavePolicyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeavePolicy.objects.all()
    serializer_class = LeavePolicySerializer


class LeavetableList(generics.ListCreateAPIView):
    queryset = Leavetable.objects.all()
    serializer_class = LeavetableSerializer


class LeavetableDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leavetable.objects.all()
    serializer_class = LeavetableSerializer


class ApplyLeavesList(generics.ListCreateAPIView):
    queryset = ApplyLeaves.objects.all()
    serializer_class = ApplyLeavesSerializer


class ApplyLeavesDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplyLeaves.objects.all()
    serializer_class = ApplyLeavesSerializer


class SwipeDataList(generics.ListCreateAPIView):
    queryset = SwipeData.objects.all()
    serializer_class = SwipeDataSerializer


class SwipeDataDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = SwipeData.objects.all()
    serializer_class = SwipeDataSerializer


class AttendanceReportList(generics.ListCreateAPIView):
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer


class AttendanceReportDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer


class EmployeeShiftsList(generics.ListCreateAPIView):
    queryset = EmployeeShifts.objects.all()
    serializer_class = EmployeeShiftsSerializer


class EmployeeShiftsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeShifts.objects.all()
    serializer_class = EmployeeShiftsSerializer
