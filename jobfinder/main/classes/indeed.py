import re

from selenium.webdriver.remote.webelement import WebElement

from .job import Job

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class IndeedSearch:
    """ Handles scraping indeed job board for job roles.

        Attributes:
            driver : scraping driver to access html pages
    """

    def __init__(self, location: str = "London", title: str = None,
                 job_type: str = "temporary",
                 radius: str = "0"
                 ):
        self.driver: webdriver = webdriver.Chrome()
        if title:
            title = "q=" + title + "&"
        else:
            title = ""
        self.driver.get(
            "https://uk.indeed.com/jobs?" + title + "l=" + location +
            "&radius=" + radius + "&jt=" + job_type
        )

    def get_links(self) -> list[Job]:
        """ Scraping method to gather all listed jobs using self.driver

            Returns:
                A list of Job objects for each listed job respectively
        """
        links: list[Job] = []

        while 1:
            jobs_num: list[
                WebElement] = self.driver.find_elements_by_class_name("tapItem")
            for i in jobs_num:
                link: str = i.get_attribute("href")
                try:
                    salary: str = i.find_element_by_class_name("salary-snippet"
                                                               ).get_attribute(
                        "innerHTML"
                    )
                    no_html = re.compile("<.*?>")
                    salary = re.sub(no_html, "", salary)
                except NoSuchElementException:
                    salary: str = ""

                try:
                    i.find_element_by_class_name("jobCardShelfContainer"
                                                 ).find_element_by_class_name(
                        "jobCardShelf"
                    ).find_element_by_class_name(
                        "indeedApply"
                    )
                    difficulty: str = "Easy"
                except NoSuchElementException:
                    difficulty: str = ""
                spans: list[WebElement] = i.find_element_by_class_name(
                    "jobTitle"
                ).find_elements_by_tag_name(
                    "span"
                )
                name: str = ""
                for span in spans:
                    if not span.get_attribute("class"):
                        name: str = span.get_attribute("title")
                        break

                links.append(Job(name, link, salary, difficulty))

            try:
                ul: WebElement = self.driver.find_element_by_class_name(
                    "pagination-list"
                )
                last_btn: WebElement = ul.find_elements_by_tag_name("li")[-1]
                next_page: WebElement = last_btn.find_element_by_tag_name("a")
                self.driver.get(next_page.get_attribute("href"))
            except NoSuchElementException:
                break

        self.driver.quit()
        # return list with no duplicates
        return list(dict.fromkeys(links))
