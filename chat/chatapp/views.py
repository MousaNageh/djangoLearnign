from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView,  DeleteView, FormView
from chatapp.forms import UserForm, LoginForm, PostForm, CommentForm
from django.urls import reverse_lazy, reverse
from chatapp.models import AuthUser, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.utils import timezone
# Create your views here.


# @method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = "home.html"


@method_decorator(login_required, name='dispatch')
class Profile(DetailView):
    model = User
    context_object_name = "userinfo"
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(
            author_id__exact=self.request.user.pk)
        return context


@method_decorator(login_required, name='dispatch')
class AuthUserUpdateView(UpdateView):
    model = User
    template_name = "users/updateprofile.html"
    form_class = UserForm

    def form_valid(self, form):
        user = form.save(commit=False)
        if form.cleaned_data["password"]:
            user.set_password(form.cleaned_data["password"])
        if form.cleaned_data["user_profile"]:
            userimg = AuthUser.objects.get(user_id=self.request.user.pk)
            userimg.user_img = form.cleaned_data["user_profile"]
            userimg.save()
        user.save()
        return redirect(reverse("chatapp:profile", args=[user.pk]))


class Register(FormView):
    template_name = "auth/register.html"
    form_class = UserForm
    success_url = reverse_lazy("chatapp:home")

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            email=form.cleaned_data["email"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"])

        authuser_ = AuthUser(user=user)
        if 'user_profile' in form.cleaned_data:
            authuser_.user_img = form.cleaned_data["user_profile"]
        authuser_.save()
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.errors["invalid"] = "invlid process"
            return super().form_invalid(form)


class LoginUser(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("chatapp:home")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        login_user = authenticate(self.request, username=username,
                                  password=password)
        if login_user:
            login(self.request, login_user)
            return super().form_valid(form)
        else:
            form.errors["unauthorized"] = ": username or password are wrong"
            return super().form_invalid(form)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("chatapp:home"))
#######################################################################################


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/posts.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(published_at__lte=timezone.now()).order_by("-published_at")


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/post.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "posts/create.html"
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.authuser
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = "posts/create.html"

    def get_queryset(self):
        return Post.objects.filter(id__exact=self.kwargs["pk"])


class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/delete.html"
    success_url = reverse_lazy("chatapp:posts")


class UnapprovedPostList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/unapprovedposts.html'
    permission_required = "superuser"

    def get_queryset(self):
        return Post.objects.filter(published_at__isnull=True).order_by("-created_date")


@permission_required('superuser')
def approvepost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post:
        post.published_at = timezone.now()
        post.save()
    return redirect(reverse("chatapp:unapproved_posts"))

#########################################################
