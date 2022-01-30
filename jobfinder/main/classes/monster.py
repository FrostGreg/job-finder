from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep

from .job import Job


class MonsterSearch:
    """ Handles scraping Monster job board for job roles.

        Attributes:
            driver : scraping driver to access html pages
    """

    def __init__(self, location="London", title="", radius="5"):
        self.driver = webdriver.Chrome()

        self.driver.get(
            "https://www.monster.co.uk/jobs/search?q=" + title + "&where=" +
            location + "&rd=" + radius
        )

    """ Scraping method to gather all listed jobs using self.driver

            Returns:
                A list of Job objects for each listed job respectively
        """

    def get_links(self):
        links = []
        found = 0
        current = self.driver.current_url
        page_num = 1
        # sleep to allow time for the html to load for the driver
        sleep(5)
        while 1:
            try:
                jobs_num = WebDriverWait(self.driver, 4).until(
                    ec.presence_of_all_elements_located((By.CLASS_NAME,
                                                         "job-cardstyle__JobCardComponent-sc-1mbmxes-0")
                                                        )
                )
            except:
                self.driver.quit()
                return []

            if found == len(jobs_num):
                break

            for i in range(found, len(jobs_num)):
                name = jobs_num[i].find_element_by_class_name(
                    "job-cardstyle__JobCardTitle-sc-1mbmxes-2"
                ).get_attribute("innerHTML")
                try:
                    card_salary = jobs_num[i].find_elements_by_class_name(
                        "job-cardstyle__JobCardDetails-sc-1mbmxes-5"
                    )[1].get_attribute("innerHTML")

                    salary = card_salary.strip()

                except NoSuchElementException:
                    salary = ""
                links.append(Job(name, self.driver.current_url, salary))

            found = len(jobs_num)
            page_num += 1
            try:
                self.driver.find_element_by_class_name("qTiuX")
                break
            except NoSuchElementException:
                self.driver.get(current + "&page=" + str(page_num))

        self.driver.quit()

        return list(dict.fromkeys(links))
