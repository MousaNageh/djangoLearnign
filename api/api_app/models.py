from djongo import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)

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
    pass
  
  
