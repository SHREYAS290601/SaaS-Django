from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from visits.models import PageVisit

LOGIN_URL = settings.LOGIN_URL


def home(request):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    qs.count()
    page_qs.count()

    content = {
        "title": "Home",
        "content": "Welcome to the homepage.",
    }
    PageVisit.objects.create(path=request.path)
    html_page = "home.html"
    return render(request, html_page, content)


VALID_CODE = "ABC123"


def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get("is_allowed", False) or False
    if request.method == "POST":
        user_pw_code = str(request.POST.get("code"))
        if user_pw_code == VALID_CODE:
            is_allowed = True
            request.session["is_allowed"] = True
    if is_allowed:
        return render(request, "protected/view.html", {"title": "Protected"})
    return render(request, "protected/entry.html", {"title": "Protected"})


@login_required
def user_only_view(request, *args, **kwargs):
    return render(request, "protected/user.html", {"title": "User Only"})


@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, "protected/user.html", {"title": "Staff Only"})
