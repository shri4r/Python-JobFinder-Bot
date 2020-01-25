import lxml
import math
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException

def coffeeJobs(search_key):
    #Selenium 

    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://www.coffeejobs.com"
    location = "Australia"
    driver.get(main_url)
   
    search_input = driver.find_element_by_id("q")
    search_input.clear()
    search_input.send_keys(search_key)

    location_input = driver.find_element_by_id("l")
    location_input.clear()
    location_input.send_keys(location)
    
    search_btn = driver.find_element_by_xpath("//div[@class='siteSearch-submit']/button")
    search_btn.click()
    sleep(5)

    try:
        results_statement = driver.find_element_by_xpath("//div[@class='results-headerLeft']/span").text
        a_list = results_statement.split()
        number_of_items_found = float(a_list[0])
        number_of_iteration = number_of_items_found / 20
        number_of_iteration = math.ceil(number_of_iteration)

        #Beautifulsoup
        ua = UserAgent()
        header = {"user-agent": ua.chrome}
        soup = BeautifulSoup(driver.page_source,"lxml")
        driver.quit()

        all_the_links = soup.find_all("a",class_="jobList-title")
        result = {main_url+a["href"]:a.string for a in all_the_links}
        for key,value in result.items():
            print(key, "-->>", value)

        # Going to 2nd , 3rd and ... page
        for _ in range(int(number_of_iteration - 1)):
            next_pages_container = soup.find("ul",class_="pagination")
            a_list = next_pages_container.find_all("li")
            next_page_btn = a_list[-2]
            next_page_full_link = main_url + next_page_btn.a["href"]
        
            sleep(2)
            next_page = requests.get(next_page_full_link,headers=header)
            soup = BeautifulSoup(next_page.content, "lxml")

            all_the_links = soup.find_all("a",class_="jobList-title")
            result = {main_url+a["href"]:a.string for a in all_the_links}
            for key,value in result.items():
                print(key, "-->>", value)

    except:
        print("didnt found anything")
        driver.quit()


coffeeJobs("barista")