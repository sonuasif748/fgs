from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Organisation_Info, Department, Designation
from .serializers import Organisation_InfoSerializer, DepartmentSerializer, DesignationSerializer
from .constants import Messages

import logging
logger = logging.getLogger(__name__)


# Create your views here.


class Organisation_InfoList(generics.ListCreateAPIView):
    queryset = Organisation_Info.objects.all()
    serializer_class = Organisation_InfoSerializer


class Organisation_InfoDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organisation_Info.objects.all()
    serializer_class = Organisation_InfoSerializer
    
class DepartmentList(generics.ListCreateAPIView):
    logger.info("dept list")
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {}
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data.update(serializer.data)
            data.update({"message": Messages.created.value.format(data['dept_name'])})
        except Exception as e:
            data.update({"err_msg": Messages.already_exist.value.format(request.data['dept_name'])})
        return Response(data)


class DepartmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = super(DepartmentDetails, self).update(request, *args, **kwargs).data
        data.update({"message": Messages.updated.value.format(data['dept_name'])})
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": Messages.deleted.value.format(instance['dept_name'])})


class DesignationList(generics.ListCreateAPIView):
    logger.info("desig list")
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {}
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data.update(serializer.data)
            data.update({"message": Messages.created.value.format(data['desig_name'])})
        except Exception as e:
            data.update({"message": Messages.already_exist.value.format(request.data['desig_name'])})
        return Response(data)


class DesignationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = super(DesignationDetails, self).update(request, *args, **kwargs).data
        data.update({"message": Messages.updated.value.format(data['desig_name'])})
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": Messages.deleted.value.format(instance['desig_name'])})