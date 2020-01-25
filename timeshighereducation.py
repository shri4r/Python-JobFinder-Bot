import lxml
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

def timesHigherEducation(search_key):
    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://www.timeshighereducation.com/unijobs/searchjobs"
    first_part_of_url = "https://www.timeshighereducation.com"
    location = "Australia"
    driver.get(main_url)
    sleep(1)

    search_input = driver.find_element_by_id("keyword")
    search_input.send_keys(search_key)
    location_input = driver.find_element_by_id("location")
    location_input.clear()
    location_input.send_keys(location)
    search_btn = driver.find_element_by_xpath("//input[@value='Search']")
    search_btn.click()
    sleep(2)
    
    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome} 
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    driver.quit()

    try:
        container = soup.find("ul",attrs={"id":"listing"})
        all_the_links = container.find_all("h3",class_="lister__header")

        final_result = {first_part_of_url + link.a["href"].strip():link.a.span.string for link in all_the_links} # strip() = Remove Space at the Start and end of the string in Python 

        for key,value in final_result.items():
            print(key,"-->>",value)

        # Going to next pages
        while True:
            next_page_full_link = first_part_of_url + soup.find("a",attrs={"title":"Next page"})["href"]
            next_page = requests.get(next_page_full_link,headers=header)
            sleep(2)
            soup = BeautifulSoup(next_page.content,"lxml")

            container = soup.find("ul",attrs={"id":"listing"})
            all_the_links = container.find_all("h3",class_="lister__header")

            final_result = {first_part_of_url + link.a["href"].strip():link.a.span.string for link in all_the_links} # strip() = Remove Space at the Start and end of the string in Python 

            for key,value in final_result.items():
                print(key,"-->>",value)
    
    except:
        pass

timesHigherEducation("teacher")