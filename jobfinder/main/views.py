from django.shortcuts import render
from .classes.main import IndeedSearch, TotalJobsSearch, MonsterSearch
from django.core.exceptions import ObjectDoesNotExist
from .models import Job
from datetime import timedelta
from django.utils import timezone


# Create your views here.

def index(response):
    if response.method == "GET":
        if response.GET.get("search"):
            return result(response)
    return render(response, "main/home.html", {})


def latest_search(response):
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
    check_to_type = {"c-full": "fulltime",
                     "c-part": "parttime",
                     "c-temp": "temporary",
                     "c-vol": "volunteer"}
    Job.objects.all().delete()
    for element in response.GET:
        if element in check_to_type:
            if response.GET.get("c-indeed"):
                new = IndeedSearch(location=location, job_type=check_to_type[element], title=title, radius=radius)
                for job in new.get_links():
                    Job(search=title, title=job.title, link=job.link, pay=job.pay, difficulty=job.difficulty,
                        radius=radius, location=location, type=check_to_type[element], board="indeed").save()

            if response.GET.get("c-totaljobs") and element != "c-vol":
                if radius == "25":
                    radius = "20"
                new = TotalJobsSearch(location=location, job_type=check_to_type[element], title=title,
                                      radius=radius)
                for job in new.get_links():
                    Job(search=title, title=job.title, link=job.link, pay=job.pay, difficulty=job.difficulty,
                        radius=radius, location=location, type=check_to_type[element], board="totaljobs").save()

            if response.GET.get("c-monster") and int(radius) >= 5:
                if radius == "25":
                    radius = "20"
                new = MonsterSearch(location=location, title=title, radius=radius)
                for job in new.get_links():
                    Job(search=title, title=job.title, link=job.link, pay=job.pay, difficulty=job.difficulty,
                        radius=radius, location=location, type=check_to_type[element], board="monster").save()


def result(response):
    if response.GET.get("latest"):
        current_jobs = Job.objects.filter(search=response.GET.get("job-title").strip())
        if len(current_jobs) > 0:
            date = current_jobs[0].date
            time_to_refresh = date + timedelta(minutes=30)
            if timezone.now() > time_to_refresh:
                latest_search(response)
        else:
            latest_search(response)

    if response.method == "GET":
        if len(Job.objects.filter(search=response.GET.get("job-title").strip())) == 0:
            latest_search(response)
        check_to_type = {"c-full": "fulltime",
                         "c-part": "parttime",
                         "c-temp": "temporary",
                         "c-vol": "volunteer"}
        indeed_jobs = []
        totaljobs_jobs = []
        monster_jobs = []
        for element in response.GET:
            if element in check_to_type:
                indeed_jobs += list(
                    Job.objects.filter(search=response.GET.get("job-title").strip(), type=check_to_type[element],
                                       board="indeed"))
                totaljobs_jobs += list(
                    Job.objects.filter(search=response.GET.get("job-title").strip(), type=check_to_type[element],
                                       board="totaljobs"))
                monster_jobs += list(
                    Job.objects.filter(search=response.GET.get("job-title").strip(), type=check_to_type[element],
                                       board="monster_jobs"))

        if not response.GET.get("c-indeed"):
            indeed_jobs = []

        if not response.GET.get("c-totaljobs"):
            totaljobs_jobs = []

        if not response.GET.get("c-monster"):
            monster_jobs = []

        return render(response, "main/result.html", {"indeed_jobs": indeed_jobs, "totaljobs_jobs": totaljobs_jobs,
                                                     "monster_jobs": monster_jobs,
                                                     "found": len(indeed_jobs) + len(totaljobs_jobs) + len(
                                                         monster_jobs)})
