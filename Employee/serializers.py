from rest_framework import serializers
from .models import Employee_Info

class Employee_InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Info
        fields = '__all__'
        
        
