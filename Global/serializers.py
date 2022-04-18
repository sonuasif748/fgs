from rest_framework import serializers
from .models import Country, Cont_State, Financial_Year


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        
        
class Cont_StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cont_State
        fields = '__all__'
        
        
class Financial_YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financial_Year
        fields = '__all__'


