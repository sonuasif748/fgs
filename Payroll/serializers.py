from rest_framework import serializers
from .models import *
from InTax.serializers import Salary_HeadsSerializer
from drf_writable_nested import WritableNestedModelSerializer


        
class Company_SalsetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySalsetup
        fields = '__all__'

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['Particulars'] = Salary_HeadsSerializer(instance.particulars).data
            return rep
        
        
class Co_SalsetupSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    companysalsetup_set = Company_SalsetupSerializer(many=True)
    class Meta:
        model = CoSalsetup
        fields = '__all__'


class EmpMonthCtcMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpMonthCtcMaster
        fields = '__all__'


class EmpMonPayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpMonPayroll
        fields = '__all__'


class EmpCtcMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpCtcMaster
        fields = '__all__'