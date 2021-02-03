from django.shortcuts import render, redirect
from django.urls import reverse
from userApp.forms import UserForm, UserProfile, UserLogin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.


@login_required
def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfile(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return render(request, "index.html")
    return render(request,  "register.html", {"user_form": UserForm(), "profile_form": UserProfile()})


def user_login(request):
    if request.method == "POST":
        user_login = UserLogin(request.POST)
        if user_login.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('auth:index'))
                else:
                    return HttpResponse("acount is not active ")
            else:
                print("someone try to access your acount")
        else:
            return render(request, "login.html", {
                'errors': user_login.errors,
                'username': request.POST.get("username"),
                'password': request.POST.get("password")})
    return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("auth:index"))
