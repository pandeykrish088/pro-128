from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
from selenium import webdriver 
import requests
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("/Users/apoorvelous/Downloads/chromedriver")

browser.get(START_URL)
time.sleep(10)

star_data = []
headers = ["name", "distance", "mass", "radius"]

def scrape():
    

    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")

        for ul_tag in soup.find_all("ul", attrs={"class", "brightest-stars"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []

            for index, li_tag in enumerate(li_tags):

                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])

                else:
                    try:
                        temp_list.append(li_tag.contents[0])

                    except:
                        temp_list.append("")

            star_data.append(temp_list)
            
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(star_data)
scrape()


new_stars_data = []

def scrape_more_data():
    url = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    star_table = soup.find_all('table')

    table_rows = star_table[7].find_all('tr')

    for tr_tag in soup.find_all("tr", attrs = {"class": "fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list = []

        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attrs = {"class": "value"})[0].contents[0])
        
            except:
                temp_list.append("")
        
        new_stars_data.append(temp_list)

scrape()

for data in star_data:
    scrape_more_data(data[5])

final_star_data = []

for index, data in enumerate(star_data):
    final_star_data.append(data + final_star_data[index])

with open("Final_star.csv", "w") as f:
    csvWriter = csv.writer(f)
    csvWriter.writerow(headers)
    csvWriter.writerows(final_star_data)