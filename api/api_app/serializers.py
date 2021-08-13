from rest_framework import serializers 
from .models import User,Expense,Image
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer): 
  password = serializers.CharField(min_length=6,max_length=68,write_only=True)
  class Meta:
    model = User 
    fields = ["username","email","password"]
  
  

  def validate(self, attrs):
    email = attrs.get("email","")
    username = attrs.get("username","")
    password = attrs.get("password","")
    if not username.isalnum(): 
      raise serializers.ValidationError("username must be alpha numeric ",status.HTTP_400_BAD_REQUEST)
    return super().validate(attrs)

    def create(self, validated_data):
      return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255,required=True)
  password = serializers.CharField(max_length=68,min_length=6,required=True,write_only=True) 

  def validate(self, attrs):
    print(attrs.get("email"))
    email = attrs.get("email","")
    password = attrs.get("password","")
    user = authenticate(email=email,password=password)
    
    if not user : 
      raise AuthenticationFailed(detail="email or password is not valid",code=status.HTTP_401_UNAUTHORIZED)
    elif not user.is_verified : 
      raise AuthenticationFailed(detail="email is not activated",code=status.HTTP_400_BAD_REQUEST)
    
    return {"user":{
            "username":user.username , 
            "email":user.email,
            "tokens":user.tokens()
          }}
    
class ExpenseSerializer(serializers.ModelSerializer): 
  class Meta : 
    model = Expense
    fields = "__all__"


class ImageSerializer(serializers.Serializer): 
  img = serializers.ImageField()
