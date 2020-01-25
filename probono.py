import lxml
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

def probonoAustralia(search_key):
    driver = webdriver.Chrome(executable_path=r"G:/Shah/Git proje/Job-Finder-Bot/chromedriver.exe")
    main_url = "https://probonoaustralia.com.au/jobs"
    driver.get(main_url)
    sleep(4)

    try:
        close_subscribe_btn = driver.find_element_by_xpath("//span[@class='et_bloom_close_button']")
        close_subscribe_btn.click()
    except:
        pass

    search_input = driver.find_element_by_xpath("//input[@id='s' and @name='q']")
    search_input.send_keys(search_key)
    sleep(0.5)
    location_dropdown = driver.find_element_by_xpath("//select[@id='locationform']/option[contains(text(),'Australia')]")
    location_dropdown.click()
    
    search_btn = driver.find_element_by_xpath("//input[@id='searchsubmitGtG' and @value='Search']")
    search_btn.click()
    sleep(2)
    
    # Beautifulsoup
    ua = UserAgent()
    header = {"user-agent": ua.chrome} 
    soup = BeautifulSoup(driver.page_source,"lxml")
    driver.close()
    driver.quit()

    try:
        container = soup.find_all("a",class_="postTitle")

        final_result = {a["href"]:a.string for a in container}

        for key,value in final_result.items():
            print(key,"-->>",value)

        # Going to next pages
        while True:
            container_of_links = soup.find("div",class_="paginate-purple")
            next_page_full_link = main_url + container_of_links.find("a",text = "Next")["href"]

            sleep(2)
            next_page = requests.get(next_page_full_link,headers=header)
            soup = BeautifulSoup(next_page.content,"lxml")

            container = soup.find_all("a",class_="postTitle")

            final_result = {a["href"]:a.string for a in container}

            for key,value in final_result.items():
                print(key,"-->>",value)
    except:
        pass

probonoAustralia("account")