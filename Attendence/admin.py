from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Custom)
admin.site.register(LeavePolicy)
admin.site.register(Leavetable)
admin.site.register(ApplyLeaves)
admin.site.register(SwipeData)
admin.site.register(AttendanceReport)
admin.site.register(EmployeeShifts)