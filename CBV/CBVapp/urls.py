from django.urls import path
from CBVapp.views import CBVview, CBVTempleteView, SchoolListView, SchoolDetailView, SchoolCreateView, SchoolUpdateView, SchoolDeleteView
app_name = "CBV"
urlpatterns = [
    path("temp/", CBVview.as_view()),
    path("", CBVTempleteView.as_view()),
    path("list/", SchoolListView.as_view(), name="list"),
    path("list/<int:pk>", SchoolDetailView.as_view(), name="detail"),
    path("createschool/", SchoolCreateView.as_view(), name="createschool"),
    path("updateschool/<int:pk>", SchoolUpdateView.as_view(), name="updateschool"),
    path("deleteschool/<int:pk>", SchoolDeleteView.as_view(), name="deleteschool"),


]
