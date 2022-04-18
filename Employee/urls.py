from django.urls import path
from .views import Employee_InfoList, Employee_InfoDetails

urlpatterns = [    
    path('emp/', Employee_InfoList.as_view(), name='emp_list'),
    path('emp/<int:pk>', Employee_InfoDetails.as_view(), name='emp_details'),
    
        
]