from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


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

class TotalJobs:
    pass


if __name__ == "__main__":
    new = IndeedSearch()

    print(new.get_length())

    result = new.get_links()
    for link in result:
        print(link)

    print(len(result), "jobs found")
