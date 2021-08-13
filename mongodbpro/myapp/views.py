from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import User, FriendRequest
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from myapp.forms import UserForm, LoginForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
# from django.views.decorators.csrf import csrf_exempt
# Create your views h


class Home(TemplateView):
    template_name = "home.html"


class Register(CreateView):
    model = User
    template_name = "auth/register.html"
    form_class = UserForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        auth_user = authenticate(
            self.request, username=user.username, password=form.cleaned_data["password"])
        if auth_user:
            login(self.request, auth_user)
            return super().form_valid(form)
        else:
            form.errors["invliad proceess"] = "can't login "
            return super().form_invalid(form)


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.errors["unauthenticated"] = ": username or password is not correct try again "
            return super().form_invalid(form)


class ProfileDetail(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'profile'


class UserUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    form_class = UserForm
    template_name = "auth/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context

    def form_valid(self, form):
        old_image_name = User.objects.get(
            id=self.request.user.id).user_img.name
        user = form.save(commit=False)
        if form.cleaned_data["password"]:
            user.set_password(form.cleaned_data["password"])

        if "user_img" in self.request.FILES:
            user.delete_img(old_image_name)
            user.user_img = self.request.FILES["user_img"]
        user.save()
        return super().form_valid(form)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("myapp:login"))

###############################################################################################


class UsersList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        friends_id = []
        requests = FriendRequest.objects.filter(
            Q(from_user_id__exact=self.request.user.pk) | Q(to_user_id__exact=self.request.user.pk)).all()
        for re in requests:
            if not re.approved:
                data.append(re.to_user_id)
            else:
                friends_id.append(re.to_user_id)
        context["requstsIDs"] = data
        context["friends"] = friends_id
        return context


@login_required
def addFriend(request, pk):
    friend_to_add = User.objects.get(id__exact=pk)
    user = User.objects.get(id__exact=request.user.pk)
    FriendRequest.objects.create(from_user=user, to_user=friend_to_add)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def removeRequest(request, pk):
    user = User.objects.get(id__exact=request.user.pk)
    relationship = FriendRequest.objects.get(
        Q(to_user_id__exact=pk) & Q(from_user__exact=user.pk))
    relationship.delete()
    if request.path == f"/people/removerequest/{pk}":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
