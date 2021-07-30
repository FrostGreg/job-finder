from django.shortcuts import render
from .classes.main import IndeedSearch


# Create your views here.

def index(response):
    if response.method == "GET":
        if response.GET.get("search"):
            return result(response)
    return render(response, "main/home.html", {})


def result(response):
    location = response.GET.get("job-location")
    if len(location) == 0:
        location = None
    title = response.GET.get("job-title")
    radius = response.GET.get("radius")
    jobs = []
    check_to_type = {"c-full": "fulltime",
                     "c-part": "parttime",
                     "c-vol": "volunteer"}
    for element in response.GET:
        if element in check_to_type:
            new = IndeedSearch(location=location, job_type=check_to_type[element], title=title, radius=radius)
            jobs += new.get_links()

    new = IndeedSearch(location=location, title=title, radius=radius)
    jobs += new.get_links()

    return render(response, "main/result.html", {"jobs": jobs})
