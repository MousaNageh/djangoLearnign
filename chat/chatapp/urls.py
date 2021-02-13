from django.urls import path
from chatapp.views import (Home, Register, LoginUser, logout_view,
                           Profile,  PostListView, PostDetail, PostCreateView,
                           PostUpdateView, PostDeleteView, UnapprovedPostList, approvepost, AuthUserUpdateView)
from django.conf import settings
from django.conf.urls.static import static
app_name = "chatapp"
urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("register/", Register.as_view(), name='register'),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout", logout_view, name="logout"),
    path("profile/<int:pk>/", Profile.as_view(), name="profile"),
    path("profile/<int:pk>/edit",
         AuthUserUpdateView.as_view(), name="update_profile"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("unapprovedposts/", UnapprovedPostList.as_view(), name="unapproved_posts"),
    path("unapprovedposts/approve/<int:pk>", approvepost, name="approve"),
    path("posts/<int:pk>/", PostDetail.as_view(), name="post"),
    path("posts/create/", PostCreateView.as_view(), name="createpost"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="updatepost"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="deletepost"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
