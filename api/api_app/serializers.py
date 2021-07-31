from rest_framework import serializers 
from .models import User
from rest_framework import status
class RegisterSerializer(serializers.ModelSerializer): 
  password = serializers.CharField(min_length=6,max_length=68)
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
    