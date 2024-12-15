#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class GoogleMapScraper:
    def __init__(self):
        self.output_file_name = "dhaturi_extraction.csv"
        self.headless = False
        self.driver = None
        self.unique_check = []

    def config_driver(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=options)
        self.driver = driver

    def save_data(self, data):
        header = ['company_name',"address", 'email', 'phone', 'website']
        with open(self.output_file_name, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def parse_contact(self, business):
        try:
            contact = business.find_elements(By.CLASS_NAME, "W4Efsd")[3].text.split("·")[-1].strip()
        except:
            contact = ""

        if "+1" not in contact:
            try:
                contact = business.find_elements(By.CLASS_NAME, "W4Efsd")[4].text.split("·")[-1].strip()
            except:
                contact = ""

        return contact

    def get_business_info(self):
        time.sleep(2)
        for business in self.driver.find_elements(By.CLASS_NAME, 'THOPZb'):
            name = business.find_element(By.CLASS_NAME, 'fontHeadlineSmall').text

            # Initialize variables for email,address, phone, and website
            email = ""
            address = ""
            phone = ""
            website = ""

            try:
                address = business.find_element(By.CLASS_NAME, "Io6YTe ").text()
                print(address)
            except NoSuchElementException:
                address = ""
                print(address)

            try:
                contact = business.find_elements(By.CLASS_NAME, "W4Efsd")[3].text.split("·")[-1].strip()
                if "@" in contact:
                    email = contact
                    print(email)
                else:
                    phone = contact
                    print(phone)
            except:
                pass

            try:
                website = business.find_element(By.CLASS_NAME, "CsEnBe").get_attribute("href")
                print(website)
            except NoSuchElementException:
                website = ""
                print(website)

            unique_id = "".join([name, address, email, phone, website])
            if unique_id not in self.unique_check:
                data = [name, address, email, phone, website]
                self.save_data(data)
                self.unique_check.append(unique_id)

    def load_companies(self, url):
        print("Getting business info from", url)
        self.driver.get(url)
        time.sleep(5)
        panel_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
        scrollable_div = self.driver.find_element(By.XPATH, panel_xpath)
        flag = True
        i = 0
        while flag:
            print(f"Scrolling to page {i + 2}")
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(2)

            if "You've reached the end of the list." in self.driver.page_source:
                flag = False

            self.get_business_info()
            i += 1

if __name__ == "__main__":
    search_query = "manufacturing units + Dhaturi"
    base_url = f"https://www.google.com/maps/search/{search_query}"
    
    business_scraper = GoogleMapScraper()
    business_scraper.config_driver()
    business_scraper.load_companies(base_url)


# In[ ]:




