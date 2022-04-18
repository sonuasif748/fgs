from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response


# Create your views here.


class Tax_headerList(generics.ListCreateAPIView):
    queryset = Tax_header.objects.all()
    serializer_class = Tax_headerSerializer


class Tax_headerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tax_header.objects.all()
    serializer_class = Tax_headerSerializer


class Tax_slabList(generics.ListCreateAPIView):
    queryset = Tax_slab.objects.all()
    serializer_class = Tax_slabSerializer


class Tax_slabDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tax_slab.objects.all()
    serializer_class = Tax_slabSerializer
    
    
class PT_HeaderList(generics.ListCreateAPIView):
    queryset = PT_Header.objects.all()
    serializer_class = PT_HeaderSerializer


class PT_HeaderDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = PT_Header.objects.all()
    serializer_class = PT_HeaderSerializer


class PT_SlabList(generics.ListCreateAPIView):
    queryset = PT_Slab.objects.all()
    serializer_class = PT_SlabSerializer


class PT_SlabDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = PT_Slab.objects.all()
    serializer_class = PT_SlabSerializer


class PF_EmprList(generics.ListCreateAPIView):
    queryset = PF_Empr.objects.all()
    serializer_class = PF_EmprSerializer


class PF_EmprDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = PF_Empr.objects.all()
    serializer_class = PF_EmprSerializer
    
    
class PF_EmpList(generics.ListCreateAPIView):
    queryset = PF_Emp.objects.all()
    serializer_class = PF_EmpSerializer


class PF_EmpDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = PF_Emp.objects.all()
    serializer_class = PF_EmpSerializer
    
    
class Esi_RatecardList(generics.ListCreateAPIView):
    queryset = Esi_Ratecard.objects.all()
    serializer_class = Esi_RatecardSerializer


class Esi_RatecardDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Esi_Ratecard.objects.all()
    serializer_class = Esi_RatecardSerializer
    
    
class Salary_HeadsList(generics.ListCreateAPIView):
    queryset = Salary_Heads.objects.all()
    serializer_class = Salary_HeadsSerializer


class Salary_HeadsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salary_Heads.objects.all()
    serializer_class = Salary_HeadsSerializer
    
class ExemptionsList(generics.ListCreateAPIView):
    queryset = Exemptions.objects.all()
    serializer_class = ExemptionsSerializer


class ExemptionsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exemptions.objects.all()
    serializer_class = ExemptionsSerializer
    
    
class Chp_VIA_DeductionsList(generics.ListCreateAPIView):
    queryset = Chp_VIA_Deductions.objects.all()
    serializer_class = Chp_VIA_DeductionsSerializer


class Chp_VIA_DeductionsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chp_VIA_Deductions.objects.all()
    serializer_class = Chp_VIA_DeductionsSerializer
    
    
class Sec16_DeduList(generics.ListCreateAPIView):
    queryset = Sec16_Dedu.objects.all()
    serializer_class = Sec16_DeduSerializer


class Sec16_DeduDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sec16_Dedu.objects.all()
    serializer_class = Sec16_DeduSerializer


class FactoriesActList(generics.ListCreateAPIView):
    queryset = FactoriesAct.objects.all()
    serializer_class = FactoriesActSerializer


class FactoriesActDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = FactoriesAct.objects.all()
    serializer_class = FactoriesActSerializer


class ShopEstablishmentList(generics.ListCreateAPIView):
    queryset = ShopEstablishment.objects.all()
    serializer_class = ShopEstablishmentSerializer


class ShopEstablishmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopEstablishment.objects.all()
    serializer_class = ShopEstablishmentSerializer
