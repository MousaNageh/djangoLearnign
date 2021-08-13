from djongo import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
import os
from rest_framework_simplejwt.tokens import RefreshToken
# from django.core.validators import FileExtensionValidator
class UserManger(BaseUserManager): 
  
  def create_user(self,username,email,password=None):
  
    if username is None : 
      raise TypeError("username must be provided")
    if email is None : 
      raise TypeError("email must be provided")
    user = self.model(username=username,email=self.normalize_email(email))
    user.set_password(password) 
    user.save(using=self._db)
    return user
  
  def create_superuser(self,username,email,password=None):
    if password is None : 
      raise TypeError("password must be provided")
    user = self.create_user(username,email,password)
    user.is_superuser = True 
    user.is_staff = True
    user.save(using=self._db)
    return user 

class User(AbstractBaseUser,PermissionsMixin):
  username = models.CharField( max_length=255,unique=True,db_index=True)
  email = models.EmailField( max_length=255,unique=True,db_index=True)
  is_verified = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ["username",]
  
  objects = UserManger()

  def __str__(self):
      return self.email
  
  def tokens(self): 
    token = RefreshToken.for_user(self)
    return {
      'refresh':str(token) , 
      'access':str(token.access_token)
    }
  
CATEGORY=[
    ("ONLINE_SERVIESE","online_servies"),
    ("ONLINE","oneline"),
    ("TEST","test"),
    ("BLANK",""),
    ("NULL",None)
  ]

class ArrayFieldModel(models.Model): 
  name = models.CharField(max_length=50,blank=True,null=True)
  class Meta: 
    abstract = True


class EmbeddedFieldModel(models.Model): 
  name = models.CharField(max_length=50,blank=True,null=True)
  class Meta: 
    abstract = True

class Image(models.Model): 
  img = models.FileField(upload_to="drug")
  

class Expense(models.Model): 
  category = models.CharField(max_length=50)
  amunt = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
  price = models.PositiveIntegerField(blank=True , null=True)
  array = models.ArrayField(model_container=ArrayFieldModel)
  embedded = models.EmbeddedField(model_container=EmbeddedFieldModel)
  imgs = models.JSONField(default=[])