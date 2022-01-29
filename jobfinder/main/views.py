from django.shortcuts import render
from .classes.main import IndeedSearch, TotalJobsSearch, MonsterSearch
from .models import Job
from datetime import timedelta
from django.utils import timezone


# Create your views here.

def index(response) -> render:
    """ Decides which page to be rendered given certain actions

        Args:
            response : http request from the user

        Returns:
            render: The rendered HTML page

    """
    if response.method == "GET":
        if response.GET.get("search"):
            return result(response)
    return render(response, "main/home.html", {})


def latest_search(response) -> None:
    """ Triggers the scraper with the user request and stores the returned
    value in the database.

        Args:
            response : http request from the user

        Returns:
            None
    """
    # doesnt need further input validation as default values are used
    location = response.GET.get("job-location").strip().lower()
    title = response.GET.get("job-title").strip().lower()

    radius = response.GET.get("radius")
    check_to_type = {"c-full": "fulltime",
                     "c-part": "parttime",
                     "c-temp": "temporary",
                     "c-vol": "volunteer"}

    totalJobsTemp = {"c-full": "permanent",
                     "c-part": "part-time",
                     "c-temp": "temporary",
                     "c-vol": "volunteer"}
    for element in response.GET:
        if element in check_to_type:
            if response.GET.get("c-indeed"):
                new = IndeedSearch(location=location,
                                   job_type=check_to_type[element], title=title,
                                   radius=radius
                                   )
                for job in new.get_links():
                    Job(search=title, title=job.title, link=job.link,
                        pay=job.pay, difficulty=job.difficulty,
                        radius=radius, location=location,
                        type=check_to_type[element], board="indeed"
                        ).save()

            if response.GET.get("c-totaljobs") and element != "c-vol":
                if radius == "25":
                    radius = "20"
                new = TotalJobsSearch(location=location,
                                      job_type=totalJobsTemp[element],
                                      title=title,
                                      radius=radius
                                      )
                for job in new.get_links():
                    Job(search=title, title=job.title, link=job.link,
                        pay=job.pay, difficulty=job.difficulty,
                        radius=radius, location=location,
                        type=check_to_type[element], board="totaljobs"
                        ).save()

            if response.GET.get("c-monster"):
                if radius == "25":
                    radius = "20"
                if int(radius) <= 5:
                    radius = "5"
                new = MonsterSearch(location=location, title=title,
                                    radius=radius
                                    )
                for job in new.get_links():
                    Job(search=title, title=job.title, link=job.link,
                        pay=job.pay, difficulty=job.difficulty,
                        radius=radius, location=location,
                        type=check_to_type[element], board="monster"
                        ).save()


def remove_outdated_searches() -> None:
    """ Cleans the database of any outdated searches. An outdated search is
    one older than 30 minutes

        Return:
            None
    """
    scheduled_refresh = timezone.now() - timedelta(minutes=30)
    outdated = Job.objects.filter(date__lte=scheduled_refresh)
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
    relevant = Job.objects.filter(search=search, location=location)
    relevant.delete()


def result(response) -> render:
    """ Queries the database from the user input to render the job search
    pages. Triggers deleting of old values and new searches

        Args:
            response : http request from the user

        Returns:
            render : The rendered web page that includes all the scraping
            results
    """
    if response.method == "GET":
        remove_outdated_searches()

        title = response.GET.get("job-title").strip().lower()
        location = response.GET.get("job-location").strip().lower()

        current_jobs = Job.objects.filter(search=title, location=location)

        if len(current_jobs) == 0 or response.GET.get("latest"):
            remove_relevant_searches(title, location)
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
                    Job.objects.filter(search=title,
                                       type=check_to_type[element],
                                       board="indeed"
                                       )
                )
                totaljobs_jobs += list(
                    Job.objects.filter(search=title,
                                       type=check_to_type[element],
                                       board="totaljobs"
                                       )
                )
                monster_jobs += list(
                    Job.objects.filter(search=title,
                                       type=check_to_type[element],
                                       board="monster"
                                       )
                )

        if not response.GET.get("c-indeed"):
            indeed_jobs = []

        if not response.GET.get("c-totaljobs"):
            totaljobs_jobs = []

        if not response.GET.get("c-monster"):
            monster_jobs = []

        return render(response, "main/result.html",
                      {"indeed_jobs": indeed_jobs,
                       "totaljobs_jobs": totaljobs_jobs,
                       "monster_jobs": monster_jobs,
                       "found": len(indeed_jobs) + len(totaljobs_jobs) +
                                len(monster_jobs)}
                      )
