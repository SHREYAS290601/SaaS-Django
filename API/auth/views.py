from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        username = request.POST["user"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Done")
            return redirect("/")
        else:
            return HttpResponse("Invalid login")
    return render(request, "auth/login.html")


def registeration(request):
    if request.method == "POST":
        user = request.POST["user"]
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            User.objects.create_user(user, email=email, password=password)
        except Exception as e:
            return HttpResponse(f"Error {e}")
        return redirect("/")
    return render(request, "auth/register.html")
