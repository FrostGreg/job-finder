from django.shortcuts import render
from .classes.main import IndeedSearch, TotalJobsSearch


# Create your views here.

def index(response):
    if response.method == "GET":
        if response.GET.get("search"):
            return result(response)
    return render(response, "main/home.html", {})


def result(response):
    location = response.GET.get("job-location").replace(" ", "")
    title = response.GET.get("job-title").strip()

    if len(location) == 0:
        location = None
    elif not location.isalpha():
        location = None

    if len(title) == 0:
        title = None
    elif not title.isalpha():
        title = None

    radius = response.GET.get("radius")
    indeed_jobs = []
    totaljobs_jobs = []
    check_to_type = {"c-full": "fulltime",
                     "c-part": "parttime",
                     "c-temp": "temporary",
                     "c-vol": "volunteer"}
    for element in response.GET:
        if element in check_to_type:
            if response.GET.get("c-indeed"):
                new = IndeedSearch(location=location, job_type=check_to_type[element], title=title, radius=radius)
                indeed_jobs += new.get_links()
            if response.GET.get("c-totaljobs"):
                new = TotalJobsSearch(location=location, job_type=check_to_type[element], title=title, radius=radius)
                totaljobs_jobs += new.get_links()

    return render(response, "main/result.html", {"indeed_jobs": indeed_jobs, "totaljobs_jobs": totaljobs_jobs})
