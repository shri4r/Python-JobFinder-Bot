import lxml
import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

def jora(search_key):
    # Selenium

    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://au.jora.com"
    location = "Australia"
    driver.get(main_url)
    sleep(1)
    search_input = driver.find_element_by_id("q")
    search_input.send_keys(search_key)
    location_input = driver.find_element_by_id("l")
    location_input.clear()
    location_input.send_keys(location)
    search_btn = driver.find_element_by_id("fj")
    search_btn.click()
    sleep(2)
    
    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome} 
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    driver.quit()

    try:
        container = soup.find_all("li",class_="result") # finds all the link containers which are a <li> tag
        final_result = {main_url + li.find("a")["href"]:li.find("a").string for li in container}

        for key,value in final_result.items():
            print(key,"-->>",value)
    
        # Going to other pages
        while True:
            next_page_links_container = soup.find("div",class_="pagination")
            next_page_btn = next_page_links_container.find("a",text=re.compile("Next >"))
            next_page_full_link = main_url + next_page_btn["href"]

            sleep(3)
            next_page = requests.get(next_page_full_link,headers=header)
            sleep(1)
            soup = BeautifulSoup(next_page.content,"lxml")

            container = soup.find_all("li",class_="result") # finds all the link containers which are a <li> tag
            final_result = {main_url + li.find("a")["href"]:li.find("a").string for li in container}

            for key,value in final_result.items():
                print(key,"-->>",value)
    except:
        pass
        

jora("python")