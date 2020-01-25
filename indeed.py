import re
import lxml
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

def indeed(search_key):
    #Selenium

    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://au.indeed.com"
    location = "Australia"
    driver.get(main_url)
    sleep(1)
    search_input = driver.find_element_by_xpath("//input[@id='text-input-what']")
    search_input.send_keys(search_key)
    location_input = driver.find_element_by_xpath("//input[@id='text-input-where']")
    location_input.clear()
    location_input.send_keys(location)
    search_btn = driver.find_element_by_xpath("//button[contains(text(),'Find Jobs')]")
    search_btn.click()
    sleep(5)

    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome}
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    driver.quit()
    
    try:
        all_the_divs = soup.find_all("div",class_="jobsearch-SerpJobCard unifiedRow row result clickcard")

        final_result = {main_url + div.find("a")["href"]:div.find("a")["title"] for div in all_the_divs}

        for key,value in final_result.items():
            print(key, "-->>", value)
    except:
        pass

    #going to 2nd, 3rd and ... pages
    while True:
        try:
            container_div = soup.find("div",class_='pagination')
            span = container_div.find("span",text = re.compile('Next'),class_='np') #span hai ke kalame previous va next toshone

            next_page_href = span.parent.parent["href"]   #href next page
            next_page_full_link = main_url + next_page_href #full link next page

            next_page = requests.get(next_page_full_link,headers=header)
            soup = BeautifulSoup(next_page.content,"lxml")

            test = soup.find("div",attrs={"id":"searchCount"}) #This line should be deleted in the final version becuase it's just a test to see if we are in the right page
            print(test.string) #This line should be deleted in the final version becuase it's just a test to see if we are in the right page

            table = soup.find("td",attrs={"id":"resultsCol"})

            all_the_divs = table.find_all("div",class_="jobsearch-SerpJobCard unifiedRow row result")

            final_result = {main_url + div.find("a")["href"]:div.find("a")["title"] for div in all_the_divs}

            for key,value in final_result.items():
                print(key, "-->>", value)

        except AttributeError:
            break
    
indeed("python developer")