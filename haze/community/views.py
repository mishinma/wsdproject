from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "community/index.html")
    # return HttpResponse("Hello World!")

