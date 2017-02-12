from django.shortcuts import render


def index(request):
    user = request.user
    return render(request, "base/index.html", {'user': user})
