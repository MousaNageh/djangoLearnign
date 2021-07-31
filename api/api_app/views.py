from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status




class Register(GenericAPIView): 
  serializer_class = RegisterSerializer
  
  def post(self,request): 
    user = request.data 
    serializer = self.serializer_class(data=user)
    if serializer.is_valid(): #call validate method
        serializer.save() #call create method 
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
