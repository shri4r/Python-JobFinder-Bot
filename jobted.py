import lxml
import math
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException

def jobTed(search_key):
    # Selenium
    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://au.jobted.com"
    location = "Australia"
    driver.get(main_url)
    sleep(1)

    job_search_input = driver.find_element_by_id("what")
    job_search_input.clear()
    job_search_input.send_keys(search_key)

    sleep(1)

    location_input = driver.find_element_by_id("where")
    location_input.clear()
    location_input.send_keys(location)
    sleep(4)
    click_on_suggust = driver.find_element_by_xpath("//ul/li[@data-value='Australia']")
    click_on_suggust.click()
    sleep(2)
    search_btn = driver.find_element_by_id("searchB")
    search_btn.click()
    sleep(2)

    close_email_subs_window = driver.find_element_by_id("popup-no-button")
    close_email_subs_window.click()
    sleep(1)

    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome} 
    soup = BeautifulSoup(driver.page_source,"lxml")
    
    driver.close()
    driver.quit()

    try:
        all_the_links = soup.find_all("a",class_="res-link-job")

        final_result = {link["href"]:link.span.string for link in all_the_links}

        for key,value in final_result.items():
            print(key,"-->",value)

        # Going to 2ndm 3rd and ... pages
        number_of_jobs = soup.find("div",class_="res-counter").string # a string , example = 1 - 15 of 114
        number_of_jobs = number_of_jobs.split() # returns a list, example = ['1', '-', '15', 'of' ,'114']
        number_of_jobs = number_of_jobs[-1]
        number_of_jobs_fixed = int(''.join(c for c in number_of_jobs if c.isdigit())) # if the number is like 1,365, it converts that to 1365

        number_of_iteration = math.ceil((number_of_jobs_fixed/15))
    
        for _ in range(number_of_iteration-1):
            next_page_links_container = soup.find("div",class_="pager-wrapper") # container of next page links
            list_of_spans = next_page_links_container.find_all("span")
            full_link_of_next_page = list_of_spans[-1]["data-href"]

            next_page = requests.get(full_link_of_next_page,headers=header)
            sleep(2)
            soup = BeautifulSoup(next_page.content,"lxml")
            sleep(1.5)
            all_the_links = soup.find_all("a",class_="res-link-job")

            final_result = {link["href"]:link.span.string for link in all_the_links}

            for key,value in final_result.items():
                print(key,"-->",value)
    except:
        print("didnt find it")

jobTed("laravel")