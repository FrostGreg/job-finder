from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Job:
    def __init__(self, name: str, url: str, salary="", difficulty=""):
        self.name = name
        self.url = url
        self.salary = salary
        self.difficulty = difficulty

    def __str__(self):
        return self.name + self.difficulty


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
                try:
                    salary = i.find_element_by_class_name("salary-snippet").get_attribute("innerHTML")
                except NoSuchElementException:
                    salary = ""

                try:
                    i.find_element_by_class_name("jobCardShelfContainer")\
                        .find_element_by_class_name("jobCardShelf").find_element_by_class_name("indeedApply")
                    difficulty = " - Easy"
                except NoSuchElementException:
                    difficulty = ""
                spans = i.find_element_by_class_name("jobTitle").find_elements_by_tag_name("span")
                name = ""
                for span in spans:
                    if not span.get_attribute("class"):
                        name = span.get_attribute("title")
                        break

                links.append(Job(name, url, salary, difficulty))

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
            salary_span = self.driver.find_elements_by_class_name("gQrsAv")
            idx = 0
            for job in jobs_num:
                url = job.get_attribute("href")
                name = job.find_element_by_tag_name("h2").get_attribute("innerHTML")
                try:
                    salary = salary_span[idx].text
                except NoSuchElementException:
                    salary = ""
                links.append(Job(name, url, salary))
                idx += 1

            try:
                pagination_next = self.driver.find_elements_by_class_name("igiYgL")[-1]
                next_link = pagination_next.get_attribute("href")
                self.driver.get(next_link)
            except IndexError:
                break

        self.driver.quit()
        # return list with no duplicates
        return list(dict.fromkeys(links))


class MonsterSearch:
    def __init__(self, location="London", title="", radius="5"):
        self.driver = webdriver.Chrome()

        self.driver.get("https://www.monster.co.uk/jobs/search?q=" + title + "&where=" + location + "&rd=" + radius)

    def get_links(self):
        links = []
        found = 0
        current = self.driver.current_url
        page_num = 1
        while 1:
            try:
                jobs_num = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "results-card")))
            except:
                self.driver.quit()
                return []

            if found == len(jobs_num):
                break

            # divides 2 as it holds seperate instances for desktop and mobile version i.e. has 2 for every 1 job
            for i in range(found, len(jobs_num)//2):
                name = jobs_num[i].find_element_by_class_name("card-title").get_attribute("innerHTML")
                try:
                    card_salary = jobs_num[i].find_element_by_class_name("card-salary").find_element_by_tag_name("span")\
                        .get_attribute("innerHTML")
                    salary = card_salary.split()
                    salary = salary[0][:-5] + ' - ' + salary[3][7:]

                except NoSuchElementException:
                    salary = ""
                links.append(Job(name, self.driver.current_url, salary))

            found = len(jobs_num)
            page_num += 1
            try:
                self.driver.find_element_by_class_name("drMyVs")
                break
            except NoSuchElementException:
                self.driver.get(current + "&page=" + str(page_num))

        self.driver.quit()

        return links


if __name__ == "__main__":
    new = IndeedSearch(location="Newark", title="warehouse", job_type="temporary", radius="5")
    for i in new.get_links():
        print(i)
