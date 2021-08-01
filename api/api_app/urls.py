from django.urls import path 
from .views import Register,VerifyEmail 
urlpatterns = [
  path("register/",Register.as_view(),name="register"),
  path("register/verify_email",VerifyEmail.as_view(),name="verify_email")
]