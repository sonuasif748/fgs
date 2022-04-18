from django.urls import path
from .views import *

urlpatterns = [
    
    
    path('salsetup/', Co_SalsetupList.as_view()),
    path('salsetup/<int:pk>', Co_SalsetupDetails.as_view()),
    
    path('comp_sal/', Company_SalsetupList.as_view(), name='comp_sal_def'),
    path('comp_sal/<int:pk>', Company_SalsetupDetails.as_view(), name ='comp_sal_def'),

    path('empctc/', EmpCtcMasterList.as_view()),
    path('empctc/<int:pk>', EmpCtcMasterDetails.as_view()),

    path('empmonctc/', EmpMonthCtcMasterList.as_view()),
    path('empmonctc/<int:pk>', EmpMonthCtcMasterDetails.as_view()),

    path('empmonpay/', EmpMonPayrollList.as_view()),
    path('empmonpay/<int:pk>', EmpMonPayrollDetails.as_view()),

    path('exmpt',ExmpTaxdeclaration.as_view()),
    path('dedu',Ch6Taxdeclaration.as_view()),
    path('ex_dedu',exmpt_ch6.as_view()),
    path('ex_dedu_p',ExmptCh6TaxDecl.as_view()),
]