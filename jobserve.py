import lxml
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

def jobServe(search_key):
    # Selenium
    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://www.jobserve.com/au/en/Job-Search/"
    first_part_of_url = "https://www.jobserve.com"
    driver.get(main_url)

    sleep(1)
    search_input = driver.find_element_by_xpath("//input[@id='txtKey']")
    search_input.send_keys(search_key)
    search_btn = driver.find_element_by_xpath("//input[@id='btnSearch']")
    search_btn.click()
    sleep(2)

    change_view = driver.find_element_by_id("searchtogglelink")
    change_view.click() 
    sleep(2)
    
    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome}
    soup = BeautifulSoup(driver.page_source,"lxml")

    all_the_divs = soup.find_all("div",class_="jobListItem newjobsum") # The divs that contain the links and the titles
    final_result = {first_part_of_url + div.find("a")["href"]:div.find("a").string for div in all_the_divs}
    
    for key,value in final_result.items():
        print(key,"-->>",value)
    
    # Going to next pages
    while True:
        try:
            container = soup.find("div",attrs={"id":"jobListPagingControl"}) # a div that contains all the next page links
            next_page_full_link = first_part_of_url + container.find("a",attrs={"title":"Next Page"})["href"]
            next_page = requests.get(next_page_full_link,headers=header)
            soup = BeautifulSoup(next_page.content,"lxml")

            all_the_divs = soup.find_all("div",class_="jobListItem newjobsum") # The divs that contain the links and the titles
            final_result = {first_part_of_url + div.find("a")["href"]:div.find("a").string for div in all_the_divs}
            
            for key,value in final_result.items():
                print(key,"-->>",value)

        except TypeError:
            break
       
jobServe("python")