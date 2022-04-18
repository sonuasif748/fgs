from django.urls import path
from .views import Organisation_InfoList, Organisation_InfoDetails, DepartmentList, DepartmentDetails, DesignationList, DesignationDetails

urlpatterns = [
    path('org/', Organisation_InfoList.as_view(), name='Organisation_Info_list'),
    path('org/<int:pk>', Organisation_InfoDetails.as_view(), name='Organisation_Info_details'),
    
    path('dep/', DepartmentList.as_view(), name='department_list'),
    path('dep/<int:pk>', DepartmentDetails.as_view(), name='department_details'),
    
    path('desig/', DesignationList.as_view(), name='designation_list'),
    path('desig/<int:pk>', DesignationDetails.as_view(), name='designation_details'),

]