from django.shortcuts import render
from .classes.main import IndeedSearch


# Create your views here.

def index(response):
    if response.method == "POST":
        if response.POST.get("search"):
            return result(response)
    return render(response, "main/home.html", {})


def result(response):
    title = response.POST.get("job-title")
    radius = response.POST.get("radius")



    job_types = []
    jobs = []

    if response.POST.get("c-full"):
        job_types.append("fulltime")
    if response.POST.get("c-part"):
        job_types.append("parttime")
    if response.POST.get("c-vol"):
        job_types.append("volunteer")

    for job_type in job_types:
        new = IndeedSearch("Newark-on-Trent", job_type=job_type, title=title, radius=radius)
        jobs += new.get_links()

    new = IndeedSearch("Newark-on-Trent", title=title, radius=radius)
    jobs += new.get_links()

    return render(response, "main/result.html", {"jobs": jobs})
