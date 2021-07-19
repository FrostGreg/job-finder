from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class IndeedSearch:
    def __init__(self, location: str, job_type="temporary", radius="0"):
        self.PATH = "assets/chromedriver.exe"
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get("https://uk.indeed.com/jobs?l=" + location + "&radius=" + radius + "&jt=" + job_type)

    def get_length(self) -> str:
        total = self.driver.find_element_by_id("searchCountPages")
        total = total.text.split()[3]
        return total + " estimated jobs"

    def get_links(self) -> list[str]:
        links = []

        while 1:
            jobs_num = self.driver.find_elements_by_class_name("tapItem")
            for i in jobs_num:
                links.append(i.get_attribute("href"))

            ul = self.driver.find_element_by_class_name("pagination-list")
            last_btn = ul.find_elements_by_tag_name("li")[-1]
            try:
                next_page = last_btn.find_element_by_tag_name("a")
                self.driver.get(next_page.get_attribute("href"))
            except NoSuchElementException:
                break

        return links


if __name__ == "__main__":
    new = IndeedSearch("Newark-on-Trent")

    print(new.get_length())

    result = new.get_links()
    for link in result:
        print(link)

    print(len(result), "jobs found")
