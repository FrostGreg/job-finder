from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep

from .job import Job


class TotalJobsSearch:
    """ Handles scraping TotalJobs job board for job roles.

        Attributes:
            driver : scraping driver to access html pages
    """

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
        links = []
        sleep(5)  # wait until whole webpage is loaded
        try:
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.CLASS_NAME, "icQgnh"))
            )
        except:
            self.driver.quit()
            return []

        try:
            num_pages = self.driver.find_elements_by_class_name("gwcKwa")[
                -1].get_attribute("innerHTML")
        except IndexError:
            num_pages = 2

        for _ in range(1, int(num_pages)):
            jobs_num = self.driver.find_elements_by_class_name("icQgnh")
            salary_span = self.driver.find_elements_by_class_name("dqVVse")
            idx = 0
            for job in jobs_num:
                link = job.get_attribute("href")
                name = job.find_element_by_tag_name("h2").get_attribute(
                    "innerHTML"
                )
                try:
                    salary = salary_span[idx].text
                except NoSuchElementException:
                    salary = ""
                links.append(Job(name, link, salary))
                idx += 1

            try:
                pagination_next = \
                    self.driver.find_elements_by_class_name("igiYgL")[-1]
                next_link = pagination_next.get_attribute("href")
                self.driver.get(next_link)
            except IndexError:
                break

        self.driver.quit()
        # return list with no duplicates
        return list(dict.fromkeys(links))
