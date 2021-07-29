from django.shortcuts import render
from .classes.main import IndeedSearch


# Create your views here.

def index(response):
    if response.method == "POST":
        if response.POST.get("search"):
            new = IndeedSearch("Newark-on-Trent")

            result = new.get_links()

    return render(response, "main/home.html", {})
