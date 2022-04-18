from rest_framework import serializers
from .models import *

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = '__all__'


class LeavetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leavetable
        fields = '__all__'


class LeavePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicy
        fields = '__all__'


class ApplyLeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyLeaves
        fields = '__all__'


class SwipeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwipeData
        fields = '__all__'


class AttendanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceReport
        fields = '__all__'


class EmployeeShiftsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeShifts
        fields = '__all__'