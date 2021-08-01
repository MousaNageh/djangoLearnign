from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse

class Register(GenericAPIView): 
  serializer_class = RegisterSerializer
  
  def post(self,request): 
    user = request.data 
    serializer = self.serializer_class(data=user)
    if serializer.is_valid(): #call validate method
        serializer.save() #call create method
        
        user = User.objects.get(email=serializer.data.get("email",""))
        token = RefreshToken.for_user(user)
        current_site = get_current_site(request).domain
        relative_link = reverse("verify_email")
        abs_url = f"http://{current_site}{relative_link}?token={token.access_token}"
        email_body = f"Hi {user.username} , Click the link to verify Your Email : \n {abs_url}"
        data = {
          "domain":abs_url , 
          "subject":"Verify Your Email . ",
          "email_body":email_body
        }
        Util.send_email(data)

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  def get_queryset(self):
      return User.objects.all()
  

  def get(self,request): 
    serializer = self.serializer_class(self.get_queryset(),many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
class VerifyEmail(GenericAPIView): 
  def get(self,request): 
    pass
