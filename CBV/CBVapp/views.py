from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from CBVapp.models import School, Student
from django.urls import reverse_lazy


class CBVview(View):
    def get(self, request):
        return HttpResponse("hello world ")


class CBVTempleteView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = [1, 2, 3, 4, 5]
        return context


class SchoolListView(ListView):
    model = School
    context_object_name = 'schools'
    template_name = 'CBVapp/school_list.html'


class SchoolDetailView(DetailView):
    model = School
    context_object_name = 'school'
    template_name = 'CBVapp/school_detail.html'


class SchoolCreateView(CreateView):
    model = School
    template_name = "CBVapp/createScool.html"
    fields = '__all__'


class SchoolUpdateView(UpdateView):
    model = School
    template_name = "CBVapp/createScool.html"
    fields = '__all__'


class SchoolDeleteView(DeleteView):
    model = School
    success_url = reverse_lazy('CBV:list')
