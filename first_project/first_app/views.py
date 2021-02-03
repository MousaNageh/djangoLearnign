from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import Topic, AccessRecord, Webpage
# Create your views here.


def index(request):
    wepPages = AccessRecord.objects.order_by('date')
    date = {"AccessRecorders": wepPages}
    return render(request, "file/index.html", date)


def welcome(request):
    return render(request, "file/index.html")
