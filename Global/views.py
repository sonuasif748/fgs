from django.shortcuts import render
from .models import Country, Cont_State, Financial_Year
from .serializers import CountrySerializer, Cont_StateSerializer, Financial_YearSerializer
from rest_framework import generics

# Create your views here.


class Cont_StateList(generics.ListCreateAPIView):
    queryset = Cont_State.objects.all()
    serializer_class = Cont_StateSerializer


class Cont_StateDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cont_State.objects.all()
    serializer_class = Cont_StateSerializer


class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
    
class Financial_YearList(generics.ListCreateAPIView):
    queryset = Financial_Year.objects.all()
    serializer_class = Financial_YearSerializer


class Financial_YearDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Financial_Year.objects.all()
    serializer_class = Financial_YearSerializer

