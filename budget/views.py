from django.shortcuts import redirect, render


def index(request):
    return render(request, "budget/login.html")


def home(request):
    if request.user.is_authenticated:
        return render(request, "budget/main.html", {})
    return redirect("/")