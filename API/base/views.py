from django.shortcuts import render
from visits.models import PageVisit


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
