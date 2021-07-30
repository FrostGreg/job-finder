from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Job:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name


class IndeedSearch:
    def __init__(self, location="London", title=None, job_type="temporary", radius="0"):
        self.driver = webdriver.Chrome()
        if title:
            title = "q=" + title + "&"
        else:
            title = ""
        self.driver.get(
            "https://uk.indeed.com/jobs?" + title + "l=" + location + "&radius=" + radius + "&jt=" + job_type)

    def get_length(self) -> str:
        total = self.driver.find_element_by_id("searchCountPages")
        total = total.text.split()[3]
        return total + " estimated jobs"

    def get_links(self) -> list[Job]:
        links = []

        while 1:
            jobs_num = self.driver.find_elements_by_class_name("tapItem")
            for i in jobs_num:
                url = i.get_attribute("href")
                spans = i.find_element_by_class_name("jobTitle").find_elements_by_tag_name("span")
                name = ""
                for span in spans:
                    if not span.get_attribute("class"):
                        name = span.get_attribute("title")
                        break

                links.append(Job(name, url))

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


class TotalJobsSearch:
    def __init__(self, location="London", title=None, job_type="temporary", radius="0"):
        self.driver = webdriver.Chrome()
        if title:
            title = "/" + title
        else:
            title = ""

        self.driver.get(
            "https://totaljobs.com/jobs/" + job_type + title + "/in-" + location + "?radius=" +
            radius + "&s=header")

    def get_links(self):
        links = []
        sleep(5)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bhZgoA"))
            )
        except:
            self.driver.quit()
            return []

        try:
            num_pages = self.driver.find_elements_by_class_name("gwcKwa")[-1].get_attribute("innerHTML")
        except IndexError:
            num_pages = 2

        for _ in range(1, int(num_pages)):
            jobs_num = self.driver.find_elements_by_class_name("bhZgoA")
            for i in jobs_num:
                url = i.get_attribute("href")
                name = i.find_element_by_tag_name("h2").get_attribute("innerHTML")
                links.append(Job(name, url))

            try:
                pagination_next = self.driver.find_elements_by_class_name("igiYgL")[-1]
                next_link = pagination_next.get_attribute("href")
                self.driver.get(next_link)
            except IndexError:
                break

        self.driver.quit()
        # return list with no duplicates
        return list(dict.fromkeys(links))


if __name__ == "__main__":
    new = TotalJobsSearch("Newark", "warehouse", "temporary", "20")
    x = new.get_links()
    for job in x:
        print(job)
