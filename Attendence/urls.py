from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    #path('att',AttendanceReportView.as_view()),
    path('ltv',Leavetableviews.as_view()),

    path('custom/', CustomList.as_view(), name='custom'),
    path('custom/<int:pk>', CustomDetails.as_view(), name='custom_details'),

    path('lpolicy/', LeavePolicyList.as_view(), name='leave_policy'),
    path('lpolicy/<int:pk>', LeavePolicyDetails.as_view(), name='leave_policy_details'),

    path('ltable/', LeavetableList.as_view(), name='leave_table'),
    path('ltable/<int:pk>', LeavetableDetails.as_view(), name='leave_table_details'),

    path('applyleave/', ApplyLeavesList.as_view(), name='apply_leave'),
    path('applyleave/<int:pk>', ApplyLeavesDetails.as_view(), name='apply_leave_details'),

    path('swipedata/', SwipeDataList.as_view(), name='swipe_data'),
    path('swipedata/<int:pk>', SwipeDataDetails.as_view(), name='swipe_data_details'),

    path('attreport/', AttendanceReportList.as_view(), name='attendance_report'),
    path('attreport/<int:pk>', AttendanceReportDetails.as_view(), name='attendance_report_details'),

    path('empshift/', EmployeeShiftsList.as_view(), name='emp_shift'),
    path('empshift/<int:pk>', EmployeeShiftsDetails.as_view(), name='emp_shift_details'),
]