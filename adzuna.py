import lxml
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException

def adzuna(search_key):
    #selenium 

    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://www.adzuna.com.au/"
    location = "Australia"
    driver.get(main_url)
    sleep(1)
    search_input = driver.find_element_by_id("search_what")
    search_input.send_keys(search_key)
    location_input = driver.find_element_by_id("search_where")
    location_input.send_keys(location)
    search_btn = driver.find_element_by_xpath("//input[@type='submit']")
    search_btn.click()
    sleep(1)
    try:   
        show = driver.find_element_by_id("per_page")
        show.send_keys("50")
        sleep(4)
    except NoSuchElementException:
        pass

    #Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome}

    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.quit()

    all_divs = soup.find_all('div',class_='a')
    all_links = [div.h2.a['href'] for div in all_divs]

    for link in all_links:
        inner_page = requests.get(link,headers=header)
        inner_soup = BeautifulSoup(inner_page.content,'lxml')
        
        try:
            job_description_div = inner_soup.find("div",class_="job_details_list")
            job_location = job_description_div.dl.dt.next_element #This returns location or salary
            job_location_content = job_location.next_element.next_element.string
            final_result = {link:job_location + job_location_content} #dictinary
            for key,value in final_result.items():
                print(key,"-->",value)

        except AttributeError:
            pass

adzuna("python developer")