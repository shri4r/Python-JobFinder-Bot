import lxml
import math
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

def oneShiftJobs(search_key):
    # Selenium
    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://au.oneshiftjobs.com"
    driver.get(main_url)
    sleep(1)
    search_input = driver.find_element_by_name("keywords")
    search_input.send_keys(search_key)
    search_btn = driver.find_element_by_xpath("//button[contains(text(),'Search')]")
    search_btn.click()
    sleep(2)
    
    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome} 
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    driver.quit()
    
    container = soup.find_all("div",class_="searchResultItem")

    final_result = {main_url + div.find("a")["href"]:div.find("h2").string for div in container} 

    for key,value in final_result.items():
        print(key,"-->>",value)

    # Going to other pages
    container_of_number_of_jobs = soup.find("div",attrs={"id":"overview"})
    number_of_jobs_found = container_of_number_of_jobs.find("span").string
    number_of_jobs_fixed = int(''.join(c for c in number_of_jobs_found if c.isdigit())) # if the number is like 1,365, it converts that to 1365
    number_of_pages = math.ceil(number_of_jobs_fixed/20)

    i = 2
    while True:
        if i <= number_of_pages:
            i = str(i)
            url_pattern = "https://au.oneshiftjobs.com/search/keywords/" + search_key + "/page/" + i + "/?distance=50"
            next_page = requests.get(url_pattern,headers=header)
            i = int(i)
            i += 1 
            sleep(2)
            soup = BeautifulSoup(next_page.content,"lxml")
            sleep(1)
            container = soup.find_all("div",class_="searchResultItem")

            final_result = {main_url + div.find("a")["href"]:div.find("h2").string for div in container} 

            for key,value in final_result.items():
                print(key,"-->>",value)
        else:
            break


oneShiftJobs("Developer")