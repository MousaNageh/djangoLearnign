from django.urls import path 
from .views import Register,VerifyEmail,LoginView ,ExpenseListView,CreateExpenseView,get_all_expenses,api_add_images
urlpatterns = [
  path("register/",Register.as_view(),name="register"),
  path("register/verify_email",VerifyEmail.as_view(),name="verify_email"),
  path("login/",LoginView.as_view(),name="login"),
  path("expense/all",ExpenseListView.as_view(),name="allExpense"),
  path("expense/create",CreateExpenseView.as_view(),name="createExpense"),
  path("expense/create/test/<uuid:array_id>",get_all_expenses,name="createExpensetest"),
  path("addimg/",api_add_images,name="addimage")

]