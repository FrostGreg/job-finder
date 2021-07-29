from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class IndeedSearch:
    def __init__(self, location: str, title=None, job_type="temporary", radius="0"):
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

    def get_links(self) -> list[str]:
        links = []

        while 1:
            jobs_num = self.driver.find_elements_by_class_name("tapItem")
            for i in jobs_num:
                links.append(i.get_attribute("href"))

            try:
                ul = self.driver.find_element_by_class_name("pagination-list")
                last_btn = ul.find_elements_by_tag_name("li")[-1]
                next_page = last_btn.find_element_by_tag_name("a")
                self.driver.get(next_page.get_attribute("href"))
            except NoSuchElementException:
                break

        self.driver.quit()
        return links


if __name__ == "__main__":
    new = IndeedSearch("Newark-on-Trent")

    print(new.get_length())

    result = new.get_links()
    for link in result:
        print(link)

    print(len(result), "jobs found")
