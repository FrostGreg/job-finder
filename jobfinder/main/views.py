from typing import Any, Dict, List

from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from .classes.indeed import IndeedSearch
from .classes.totaljobs import TotalJobsSearch
from .classes.monster import MonsterSearch
from .models import Job
from datetime import datetime, timedelta
from django.utils import timezone


# Create your views here.

def index(request: HttpRequest) -> render:
    """ Decides which page to be rendered given certain actions

        Args:
            request : http request from the user

        Returns:
            render: The rendered HTML page

    """
    if request.method == "GET":
        if request.GET.get("search"):
            return result(request)
    return render(request, "main/home.html", {})


def save_indeed_jobs(title: str, location: str, element: str, radius: str
                     ) -> None:
    """ Triggers an indeed search and saves the results to the database

    Args:
        title: The title for the job search
        location: The location for the job search
        element: The job type for the job search
        radius: The radius for the job search

    Returns:
        None
    """

    new: IndeedSearch = IndeedSearch(location=location,
                                     job_type=element, title=title,
                                     radius=radius
                                     )
    for job in new.get_links():
        Job(search=title, title=job.title, link=job.link,
            pay=job.pay, difficulty=job.difficulty,
            radius=radius, location=location,
            type=element, board="indeed"
            ).save()


def save_total_jobs(title: str, location: str, element: str, radius: str
                    ) -> None:
    """ Triggers an totalJobs search and saves the results to the database

    Args:
        title: The title for the job search
        location: The location for the job search
        element: The job type for the job search
        radius: The radius for the job search

    Returns:
        None
    """

    type_to_total_jobs = {"fulltime": "permanent",
                          "parttime": "part-time",
                          "temporary": "temporary"}

    if radius == "25":
        radius = "20"
    new: TotalJobsSearch = TotalJobsSearch(location=location,
                                           job_type=type_to_total_jobs[element],
                                           title=title,
                                           radius=radius
                                           )
    for job in new.get_links():
        Job(search=title, title=job.title, link=job.link,
            pay=job.pay, difficulty=job.difficulty,
            radius=radius, location=location,
            type=element, board="totaljobs"
            ).save()


def save_monster_jobs(title: str, location: str, element: str, radius: str
                      ) -> None:
    """ Triggers an monster jobs search and saves the results to the database

    Args:
        title: The title for the job search
        location: The location for the job search
        element: The job type for the job search
        radius: The radius for the job search

    Returns:
        None
    """

    if radius == "25":
        radius = "20"
    if int(radius) <= 5:
        radius = "5"
    new: MonsterSearch = MonsterSearch(location=location, title=title,
                                       radius=radius
                                       )
    for job in new.get_links():
        Job(search=title, title=job.title, link=job.link,
            pay=job.pay, difficulty=job.difficulty,
            radius=radius, location=location,
            type=element, board="monster"
            ).save()


def get_title(request: HttpRequest) -> str:
    """ Returns the formatted title from the user response

        Attributes:
            request: user Http request

        Returns:
            str : The formatted title
    """
    return request.GET.get("job-title").strip().lower()


def get_location(request: HttpRequest) -> str:
    """ Returns the formatted location from the user response

        Attributes:
            request: user Http request

        Returns:
            str : The formatted location
    """
    return request.GET.get("job-location").strip().lower()


def latest_search(request: HttpRequest, check_to_type: dict) -> None:
    """ Triggers the scraper with the user request and stores the returned
    value in the database.

        Args:
            request : http request from the user
            check_to_type : Dictionary to convert HTML checkbox names to job
                            types

        Returns:
            None
    """
    # doesnt need further input validation as default values are used
    location: str = get_location(request)
    title: str = get_title(request)
    radius: str = request.GET.get("radius")

    for element in [value for value in request.GET if value in check_to_type]:
        if request.GET.get("c-indeed"):
            save_indeed_jobs(title, location, check_to_type[element], radius)

        if request.GET.get("c-totaljobs") and element != "c-vol":
            save_total_jobs(title, location, check_to_type[element], radius)

        if request.GET.get("c-monster"):
            save_monster_jobs(title, location, check_to_type[element], radius)


def remove_outdated_searches() -> None:
    """ Cleans the database of any outdated searches. An outdated search is
    one older than 30 minutes

        Return:
            None
    """
    scheduled_refresh: datetime = timezone.now() - timedelta(minutes=30)
    outdated: QuerySet = Job.objects.filter(date__lte=scheduled_refresh)
    outdated.delete()


def remove_relevant_searches(search: str, location: str) -> None:
    """ Removes recent relevant searches from the database in order to force
    a new search

        Args:
            search (str) : The job-title search to be removed
            location (str) : The location search to be removed

        Returns:
            None
    """
    relevant: QuerySet = Job.objects.filter(search=search, location=location)
    relevant.delete()


def result(request: HttpRequest) -> render:
    """ Queries the database from the user input to render the job search
    pages. Triggers deleting of old values and new searches

        Args:
            request : http request from the user

        Returns:
            render : The rendered web page that includes all the scraping
            results
    """

    if request.method != "GET":
        return

    check_to_type: dict[str, str] = {"c-full": "fulltime",
                                     "c-part": "parttime",
                                     "c-temp": "temporary",
                                     "c-vol": "volunteer"}

    remove_outdated_searches()

    location: str = get_location(request)
    title: str = get_title(request)

    current_jobs: QuerySet = Job.objects.filter(search=title, location=location)

    if len(current_jobs) == 0 or request.GET.get("latest"):
        remove_relevant_searches(title, location)
        latest_search(request, check_to_type)

    indeed_jobs: list[Job] = []
    total_jobs: list[Job] = []
    monster_jobs: list[Job] = []

    for element in [value for value in request.GET if value in check_to_type]:
        if request.GET.get("c-indeed"):
            indeed_jobs += list(
                Job.objects.filter(search=title,
                                   type=check_to_type[element],
                                   board="indeed"
                                   )
            )

        if request.GET.get("c-totaljobs"):
            total_jobs += list(
                Job.objects.filter(search=title,
                                   type=check_to_type[element],
                                   board="totaljobs"
                                   )
            )

        if request.GET.get("c-monster"):
            monster_jobs += list(
                Job.objects.filter(search=title,
                                   type=check_to_type[element],
                                   board="monster"
                                   )
            )

    return render(request, "main/result.html",
                  {"indeed_jobs": indeed_jobs,
                   "total_jobs": total_jobs,
                   "monster_jobs": monster_jobs,
                   "found": len(indeed_jobs) + len(total_jobs) +
                            len(monster_jobs)}
                  )
