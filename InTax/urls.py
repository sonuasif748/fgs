from django.urls import path
from .views import *

urlpatterns = [
    path('taxheader/', Tax_headerList.as_view(), name ='taxheader_list'),
    path('taxheader/<int:pk>', Tax_headerDetails.as_view(),name='taxheader_details'),
    
    path('ptheader/', PT_HeaderList.as_view()),
    path('ptheader/<int:pk>', PT_HeaderDetails.as_view()),
    
    
    path('pfempr/', PF_EmprList.as_view()),
    path('pfempr/<int:pk>', PF_EmprDetails.as_view()),
    
    path('pfemp/', PF_EmpList.as_view()),
    path('pfemp/<int:pk>', PF_EmpDetails.as_view()),
    
    path('esi/', Esi_RatecardList.as_view()),
    path('esi/<int:pk>', Esi_RatecardDetails.as_view()),
    
    
    path('sal_head/', Salary_HeadsList.as_view(), name='salary_heads'),
    path('sal_head/<int:pk>', Salary_HeadsDetails.as_view(), name ='salary_headsdetails'),
    
    
    path('exemp/', ExemptionsList.as_view(), name='exemptions'),
    path('exemp/<int:pk>', ExemptionsDetails.as_view(), name ='exemptionsdetails'),
    
    
    path('dedu/', Chp_VIA_DeductionsList.as_view(), name='deducation'),
    path('dedu/<int:pk>', Chp_VIA_DeductionsDetails.as_view(), name ='deducation_details'), 
    
    path('sec16_dedu/', Sec16_DeduList.as_view(), name='sec16_deducation'),
    path('sec16_dedu/<int:pk>', Sec16_DeduDetails.as_view(), name ='sec16_deducation_details'),

    path('facact/', FactoriesActList.as_view(), name='Facact'),
    path('facact/<int:pk>', FactoriesActDetails.as_view(), name ='facact_details'),

    path('shpact/', ShopEstablishmentList.as_view(), name='shpact'),
    path('shpact/<int:pk>', ShopEstablishmentDetails.as_view(), name ='shpact_details'),
    

]