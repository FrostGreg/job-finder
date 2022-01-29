from django.shortcuts import render
from .classes.main import IndeedSearch, TotalJobsSearch, MonsterSearch
from django.core.exceptions import ObjectDoesNotExist
from .models import Job
from datetime import timedelta
from django.utils import timezone
import re


# Create your views here.

def index(response):
    if response.method == "GET":
        if response.GET.get("search"):
            return result(response)
    return render(response, "main/home.html", {})


def latest_search(response):
    """ doesnt need further input validation as default values are used"""
    location = response.GET.get("job-location").strip()
    title = response.GET.get("job-title").strip()

    radius = response.GET.get("radius")
    check_to_type = {"c-full": "fulltime",
                     "c-part": "parttime",
                     "c-temp": "temporary",
                     "c-vol": "volunteer"}
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


def remove_outdated_searches():
    scheduled_refresh = timezone.now() - timedelta(minutes=30)
    outdated = Job.objects.filter(date__lte=scheduled_refresh)
    outdated.delete()


def remove_relevant_searches(search: str, location: str):
    relevant = Job.objects.filter(search=search, location=location)
    relevant.delete()


def result(response):
    if response.method == "GET":
        remove_outdated_searches()

        current_jobs = Job.objects.filter(search=response.GET.get("job-title").strip(),
                                          location=response.GET.get("job-location").strip())

        if len(current_jobs) == 0 or response.GET.get("latest"):
            remove_relevant_searches(response.GET.get("job-title").strip(), response.GET.get("job-location").strip())
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
