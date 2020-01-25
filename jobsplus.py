import lxml
import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

def jobsPlus(search_key):
    # Selenium

    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "http://www.jobsplus.com.au"
    driver.get(main_url)
    sleep(1)
    search_input = driver.find_element_by_xpath("//table[@id='search_form']//input")
    search_input.send_keys(search_key)
    sleep(0.5)
    search_btn = driver.find_element_by_xpath("//input[@value='   S E A R C H   ' and @type='submit']")
    search_btn.click()
    sleep(2)

    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome}
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    driver.quit()

    try:
        table = soup.find("table",attrs={"id":"joblist"}) # a table that contains all the divs and links
  
        all_the_spans = table.find_all("span",class_="job_list_title") #span which contain the links

        final_result = {span.a["href"]:span.a.string for span in all_the_spans}

        for key,value in final_result.items():
            print(key,"-->>", value)
    except AttributeError:
        pass

    # Going to 2nd , 3rd and ... pages
    while True:
        try:
            nav_page_links = soup.find("p",class_="nav_page_links") # container of next page links
            next_page_link = nav_page_links.find("a", text= re.compile(" Next ->"))
            next_page_full_link = next_page_link["href"]

            next_page = requests.get(next_page_full_link,headers=header)
            sleep(3)

            soup = BeautifulSoup(next_page.content,"lxml")

            table = soup.find("table",attrs={"id":"joblist"}) # a table that contains all the divs and links

            all_the_spans = table.find_all("span",class_="job_list_title") #span which contain the links

            final_result = {span.a["href"]:span.a.string for span in all_the_spans}

            for key,value in final_result.items():
                print(key,"-->>", value)
        except:
            break
    
jobsPlus("python developer")