import lxml
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def gumTree(search_key):
    # Selenium
 
    op = Options()
    op.add_argument('--headless')

    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe",desired_capabilities=capa,options=op)
    wait = WebDriverWait(driver, 30)
    main_url = "https://www.gumtree.com.au/jobs"
    first_part_of_url = "https://www.gumtree.com.au"
    location = "Australia"
    driver.get(main_url)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='job-search__top-tier-fields']")))
    driver.execute_script("window.stop();")
    
    search_input = driver.find_element_by_xpath("//input[@id='jlp-as-keyword']")
    search_input.send_keys(search_key)
    sleep(0.3)

    location_input = driver.find_element_by_xpath("//input[@id='search-area']")
    location_input.clear()
    location_input.send_keys(location)

    search_btn = driver.find_element_by_xpath("//button[@id='jlp-as-submit']")
    search_btn.click()
    sleep(8)
    
    # wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='panel-body panel-body--flat-panel-shadow user-ad-collection__list-wrapper']")))
    # driver.execute_script("window.stop();")

    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome}
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    driver.quit()

    try:
        container_div = soup.find_all("div", class_= "panel-body panel-body--flat-panel-shadow user-ad-collection__list-wrapper")
        container_div = container_div[1]
        all_links = container_div.find_all("a")
        final_result = {first_part_of_url+a["href"]:a["aria-label"] for a in all_links}

        for key,value in final_result.items():
           print(key, "--->>", value)
    except:
        pass

    #Going to 2nd, 3rd and ... pages
    while True:
        try:
            next_page_div = soup.find("div",class_="page-number-navigation")
            list_of_links = next_page_div.find("span",class_="icon-slider-arrow")
            next_page_link = first_part_of_url + list_of_links.parent.parent["href"]
            sleep(2)
            next_page = requests.get(next_page_link,headers=header)
            soup = BeautifulSoup(next_page.content,"lxml")

            container_div = soup.find_all("div", class_= "panel-body panel-body--flat-panel-shadow user-ad-collection__list-wrapper")
            container_div = container_div[1]
            all_links = container_div.find_all("a")
            final_result = {first_part_of_url+a["href"]:a["aria-label"] for a in all_links}

            for key,value in final_result.items():
                print(key, "--->>", value)

        except:
            print("Done")
            break

gumTree("engineer")