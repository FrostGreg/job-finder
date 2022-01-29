import re

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

    def get_length(self) -> str:
        """ Getter method for the number of estimated jobs according to indeed

            Returns:
                Formatted string containing the number of estimated jobs
        """
        total = self.driver.find_element_by_id("searchCountPages")
        total = total.text.split()[3]
        return total + " estimated jobs"

    def get_links(self) -> list[Job]:
        """ Scraping method to gather all listed jobs using self.driver

            Returns:
                A list of Job objects for each listed job respectively
        """
        links = []

        while 1:
            jobs_num = self.driver.find_elements_by_class_name("tapItem")
            for i in jobs_num:
                link = i.get_attribute("href")
                try:
                    salary = i.find_element_by_class_name("salary-snippet"
                                                          ).get_attribute(
                        "innerHTML"
                    )
                    no_html = re.compile("<.*?>")
                    salary = re.sub(no_html, "", salary)
                except NoSuchElementException:
                    salary = ""

                try:
                    i.find_element_by_class_name("jobCardShelfContainer") \
                        .find_element_by_class_name("jobCardShelf"
                                                    ).find_element_by_class_name(
                        "indeedApply"
                    )
                    difficulty = "Easy"
                except NoSuchElementException:
                    difficulty = ""
                spans = i.find_element_by_class_name("jobTitle"
                                                     ).find_elements_by_tag_name(
                    "span"
                )
                name = ""
                for span in spans:
                    if not span.get_attribute("class"):
                        name = span.get_attribute("title")
                        break

                links.append(Job(name, link, salary, difficulty))

            try:
                ul = self.driver.find_element_by_class_name("pagination-list")
                last_btn = ul.find_elements_by_tag_name("li")[-1]
                next_page = last_btn.find_element_by_tag_name("a")
                self.driver.get(next_page.get_attribute("href"))
            except NoSuchElementException:
                break

        self.driver.quit()
        # return list with no duplicates
        return list(dict.fromkeys(links))
