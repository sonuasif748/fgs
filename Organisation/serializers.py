from rest_framework import serializers
from .models import Organisation_Info, Department, Designation


class Organisation_InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation_Info
        fields = '__all__'
        

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'
