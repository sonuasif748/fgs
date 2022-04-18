from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Employee_Info
from .serializers import Employee_InfoSerializer
# Create your views here.


class Employee_InfoList(generics.ListCreateAPIView):
    queryset = Employee_Info.objects.all()
    serializer_class = Employee_InfoSerializer


class Employee_InfoDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee_Info.objects.all()
    serializer_class = Employee_InfoSerializer
    
    

