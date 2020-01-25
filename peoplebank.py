import lxml
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys

def peopleBank(search_key):
    # Selenium

    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://www.peoplebank.com.au"
    location = "Australia"
    driver.get(main_url)
    sleep(1)
    search_input = driver.find_element_by_id("query")
    search_input.send_keys(search_key)
    location_input = driver.find_element_by_xpath("//input[@autocomplete='off']")
    location_input.send_keys(location + Keys.RETURN)
    sleep(1)
    search_btn = driver.find_element_by_xpath("//button[@name='commit' and @type='submit']")
    search_btn.click()
    sleep(2)

    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome} 
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    driver.quit()

    try:
        container = soup.find_all("li",class_='job-result-item')

        final_result = {main_url + li.find("a")["href"]:li.find("a").string for li in container}

        for key,value in final_result.items():
            print(key,"-->>",value)

        # Going to next pages
        while True:
            container_of_navigation_links = soup.find("div",class_="results-nav")
            next_page_full_link = main_url + container_of_navigation_links.find("a",text="Next ›")["href"]
            next_page = requests.get(next_page_full_link,headers=header)  
            sleep(2)
            soup = BeautifulSoup(next_page.content,"lxml")

            container = soup.find_all("li",class_='job-result-item')

            final_result = {main_url + li.find("a")["href"]:li.find("a").string for li in container}

            for key,value in final_result.items():
                print(key,"-->>",value)
    except:
        pass
    
peopleBank("python")