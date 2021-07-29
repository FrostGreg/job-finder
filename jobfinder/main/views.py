from django.shortcuts import render
from .classes.main import IndeedSearch


# Create your views here.

def index(response):
    if response.method == "POST":
        if response.POST.get("search"):

            title = response.POST.get("job-title")

            radius = response.POST.get("radius")

            new = IndeedSearch("Newark-on-Trent", title=title, radius=radius)

            result = new.get_links()

            return render(response, "main/result.html", {"links": result})

    return render(response, "main/home.html", {})
