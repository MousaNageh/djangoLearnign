from django.shortcuts import render
from app.models import User
from app.forms import UserForm
# Create your views here.


def index(request):
    return render(request, "index.html", {"value": "test", "num": 12})


def users(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
    return render(request, "users.html", {"form": form})
