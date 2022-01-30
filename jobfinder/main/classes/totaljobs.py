from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep

from .job import Job


class TotalJobsSearch:
    """ Handles scraping TotalJobs job board for job roles.

        Attributes:
            driver : scraping driver to access html pages
    """
    driver: WebDriver

    def __init__(self, location="London", title=None, job_type="temporary",
                 radius="0"
                 ):
        self.driver = webdriver.Chrome()
        if title:
            title = "/" + title
        else:
            title = ""

        self.driver.get(
            "https://totaljobs.com/jobs/" + job_type + title + "/in-" +
            location + "?radius=" +
            radius + "&s=header"
        )

    """ Scraping method to gather all listed jobs using self.driver

            Returns:
                A list of Job objects for each listed job respectively
        """

    def get_links(self):
        links: list[Job] = []
        sleep(5)  # wait until whole webpage is loaded
        try:
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.CLASS_NAME, "icQgnh"))
            )
        except TimeoutException:
            self.driver.quit()
            return []

        try:
            num_pages: str = self.driver.find_elements_by_class_name("gwcKwa")[
                -1].get_attribute("innerHTML")
        except IndexError:
            num_pages = "2"

        for _ in range(1, int(num_pages)):
            jobs_num: List[
                WebElement] = self.driver.find_elements_by_class_name("icQgnh")
            salary_span: List[
                WebElement] = self.driver.find_elements_by_class_name("dqVVse")
            idx: int = 0
            for job in jobs_num:
                link: str = job.get_attribute("href")
                name: str = job.find_element_by_tag_name("h2").get_attribute(
                    "innerHTML"
                )
                try:
                    salary: str = salary_span[idx].text
                except NoSuchElementException:
                    salary = ""
                links.append(Job(name, link, salary))
                idx += 1

            try:
                pagination_next: WebElement = \
                    self.driver.find_elements_by_class_name("igiYgL")[-1]
                next_link: str = pagination_next.get_attribute("href")
                self.driver.get(next_link)
            except IndexError:
                break

        self.driver.quit()
        # return list with no duplicates
        return list(dict.fromkeys(links))
