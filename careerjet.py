import lxml
import math
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException

def careerJet(search_key):
    # Selenium

    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://www.careerjet.com.au"
    job_location = "Australia"
    driver.get(main_url)
    sleep(1)
    job_title = driver.find_element_by_xpath("//input[@id='sb_s']")
    job_title.send_keys(search_key)

    location = driver.find_element_by_xpath("//input[@id='sb_l']")
    location.clear()
    location.send_keys(job_location)

    search_btn = driver.find_element_by_xpath("//button[@value='Find']")
    search_btn.click()
    sleep(1)

    sort_by_date = driver.find_element_by_xpath("//div[@class='app_box_content']//a[contains(text(),'Date')]")
    sort_by_date.click()
    sleep(1.5)

    try:
        number_of_jobs_text = driver.find_element_by_xpath("//div[@class='search-filter-h1-prefix']//span//nobr").get_attribute("innerHTML")
        a_list = number_of_jobs_text.split()
        number_of_jobs = float(a_list[4])
        number_of_iterations = number_of_jobs / 20
        number_of_iterations = math.ceil(number_of_iterations)

        # Beautifulsoup
        ua = UserAgent()
        header = {"user-agent": ua.chrome}
        soup = BeautifulSoup(driver.page_source,"lxml")
        driver.quit()

        all_links = soup.find_all("a", class_="title-company")

        final_result = {main_url+link["href"]:link.p.string for link in all_links}

        for key,value in final_result.items():
            print(key, "-->", value)
       
        # Going to 2nd , 3rd and ... page 
        for _ in range(int(number_of_iterations - 1)): 
            next_pages_container = soup.find("div",class_="browse_container")
            next_page_links = next_pages_container.find_all("a")
            next_button_link = next_page_links[-1]
            next_button_full_link = main_url + next_button_link["href"]

            sleep(3)
            next_page = requests.get(next_button_full_link,headers=header)
            soup = BeautifulSoup(next_page.content, "lxml")

            all_links = soup.find_all("a", class_="title-company")

            final_result = {main_url+link["href"]:link.p.string for link in all_links}

            for key,value in final_result.items():
                print(key, "-->", value)

    except NoSuchElementException:
        print("didn't find anything")
        

careerJet("selenium testing automation java python")