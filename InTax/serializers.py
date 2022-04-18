from rest_framework import serializers
from .models import *
from drf_writable_nested import WritableNestedModelSerializer


class Tax_slabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax_slab
        fields = '__all__'


class Tax_headerSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    #fy = Financial_YearSerializer()
    tax_slab_set = Tax_slabSerializer(many=True)

    class Meta:
        model = Tax_header
        fields = "__all__"

    """def to_representation(self, instance):
        data = super(Tax_headerSerializer, self).to_representation(instance)
        data['fy'] = data.get('fy').get('period')
        return data"""
        
        
class PT_SlabSerializer(serializers.ModelSerializer):
    class Meta:
        model = PT_Slab
        fields = '__all__'



class PT_HeaderSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    #fy = Financial_YearSerializer()
    pt_slab_set = PT_SlabSerializer(many=True)
    
    class Meta:
        model = PT_Header
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super(PT_HeaderSerializer, self).to_representation(instance)
        #data['fy'] = data.get('fy').get('period')
        return data 
    
    
class PF_EmprSerializer(serializers.ModelSerializer):
    class Meta:
        model = PF_Empr
        fields = '__all__'
        
        
class PF_EmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PF_Emp
        fields = '__all__' 
        
        
class Esi_RatecardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Esi_Ratecard
        fields = '__all__'
        
        
class Salary_HeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary_Heads
        fields = '__all__'
        
        
class ExemptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exemptions
        fields = '__all__'
        
        
class Chp_VIA_DeductionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chp_VIA_Deductions
        fields = '__all__'
        
        
class Sec16_DeduSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sec16_Dedu
        fields = '__all__'


class FactoriesActSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoriesAct
        fields = '__all__'


class ShopEstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopEstablishment
        fields = '__all__'