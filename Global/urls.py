from django.urls import path
from .views import *

urlpatterns = [
    
    
    path('state/', Cont_StateList.as_view()),
    path('state/<int:pk>', Cont_StateDetails.as_view()),
    
    path('country/', CountryList.as_view()),
    path('country/<int:pk>', CountryDetails.as_view()),
    
    path('fy/', Financial_YearList.as_view()),
    path('fy/<int:pk>',Financial_YearDetails.as_view()),

]