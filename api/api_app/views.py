from django.shortcuts import render
from rest_framework.generics import (GenericAPIView,ListAPIView , 
CreateAPIView ,UpdateAPIView ,RetrieveAPIView , DestroyAPIView)
from .serializers import RegisterSerializer , LoginSerializer ,ExpenseSerializer,ImageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Expense,Image
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import permission_classes,api_view
import pymongo
import uuid
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


class Register(GenericAPIView): 
  serializer_class = RegisterSerializer
  
  def post(self,request): 
    user = request.data 
    serializer = self.serializer_class(data=user)
    if serializer.is_valid(): #call validate method
        User.objects.create_user(username=serializer.validated_data.get("username"),email=serializer.validated_data.get("email"),password=serializer.validated_data.get("password"))#call create method
        
        user = User.objects.get(email=serializer.data.get("email",""))
        token = RefreshToken.for_user(user)
        current_site = get_current_site(request).domain
        relative_link = reverse("verify_email")
        abs_url = f"http://{current_site}{relative_link}?token={str(token.access_token)}"
        email_body = f"Hi {user.username} , Click the link to verify Your Email : \n {abs_url}"
        data = {
          "subject":"Verify Your Email . ",
          "email_body":email_body ,
          "to_email":user.email
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
    token = request.GET.get("token","")
    try : 
      payload = jwt.decode(token,key=settings.SECRET_KEY,algorithms="HS256")
      user = User.objects.get(id=payload["user_id"])
      if not user.is_verified:
        user.is_verified = True 
      user.save()
      return Response({"success":"user is verified"},status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError : 
      return Response({"err":"token is expired"},status=status.HTTP_400_BAD_REQUEST)
    except jwt.DecodeError : 
      return Response({"err":"decode error"},status=status.HTTP_400_BAD_REQUEST)
    except :
      return Response({"err":"user not exists"},status=status.HTTP_400_BAD_REQUEST)
      
class LoginView(APIView): 
  
  def post(self,request): 
    
    serializer = LoginSerializer(data={"password":request.data.get("password"),"email":request.data.get("email")}) 
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
    
      
class ExpenseListView(ListAPIView): 
  serializer_class = ExpenseSerializer
  query_set = Expense.objects.all()
  permission_classes =(IsAuthenticated,)
  def get_queryset(self):
      return Expense.objects.all()
  

class CreateExpenseView(CreateAPIView): 
  serializer_class=ExpenseSerializer 




@api_view(["get"])
@permission_classes([IsAuthenticated,])
def get_all_expenses(request,array_id):
  id = uuid.uuid1()
  if request.method =="GET":
    id = uuid.uuid1()
    mydb = myclient["learn_api"]
    mycol = mydb["api_app_expense"]
    # mycol.update({"id":request.user.id,},{
    #   "$push":{
    #     "array":{
    #       "id":id , 
    #       "name":"test3"
    #     }
    #   }
    # })
    # mycol.update({"id":request.user.id,"array.id":array_id},{
    #   "$set":{
    #       "array.$.id":"test changed" , 
    #       "array.$.name":"test changed"
    #   }
    # })
    test = mycol.find({},{"_id":0})[0]
    print(test)
    return Response(test,status=status.HTTP_200_OK)


@api_view(["POST"])
def api_add_images(request): 
  mydb = myclient["learn_api"]
  mycol = mydb["api_app_expense"]
  img_to_delete = request.data.get("img")
  # imgeeee =  Image.objects.get(img=img_to_delete)
  # imgeeee.img.delete()
  # imgeeee.delete()
  mycol.update({"id":46},{
    "$pull":{
      "imgs":"drug/IMG_2462_UggkcLi.jpg"
    }
  })
  # images = request.FILES.getlist("img")
  # if len(images) > 0 : 
  #   for img in images : 
  #     serializer = ImageSerializer(data={"img":img})
  #     if serializer.is_valid() : 
  #       pass 
  #     else : 
  #       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  #   images_list = []
  #   for img in images :
  #     image = Image.objects.create(img=img)
  #     images_list.append(image.img.name)
  #   mycol.update({"id":46},
  #   {"$set":{"imgs":images_list}})

  
  pass