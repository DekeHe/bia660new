# !pip3 install -U selenium
!pip install selenium
!pip3 install webdriver-manager

import re, time,csv
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape(driver,url):
    fw=open('output.csv','w',encoding='utf8')
    writer=csv.writer(fw,lineterminator='\n')
    writer.writerow(['name','date','text','polarity'])

    driver.get(url)

    while True:
        driver.execute_script('window,scrollTo(0,document.body.scrollHeight)')

        reviews=driver.find_elements(by=By.CSS_SELECTOR,value='[class="row review_table_row"]')

        for review in reviews:

            name,date,text,polarity='NA','NA','NA','NA'

            try:
                pattern="unstyled bold articleLink"
                nameBox=review.find_element(by=By.CSS_SELECTOR,value='[href*="/critics/"]')
            except:
                nameBox=None

            if nameBox:name=nameBox.text

            try:
                dateBox=review.find_element(by=By.CSS_SELECTOR,value='[class="review-date subtle small"]')
            except:
                dateBox=None

            if dateBox:date=dateBox.text

            try:
                textBox=review.find_element(by=By.CSS_SELECTOR,value='[class="the_review"]')
            except:
                textBox=None

            if textBox:text=textBox.text

            try:
                polarityBox=review.find_element(by=By.CSS_SELECTOR,value='[class*="review_icon icon small"]')
            except:
                polarityBox=None

            if polarityBox:
                temp=polarityBox.get_attribute('class')

                polarity=re.search('small ([a-z]+)',temp)
                polarity=polarity.group(1)
            # print(":", polarity)
            # print(name,'\t',date,'\t',text[:10],'\t',polarity)
            writer.writerow([name,date,text,polarity])


        next=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"prev-next-paging__button-right")))

        if 'hide' in next.get_attribute('class'):
            break

        next.click()

        time.sleep(3)

    fw.close()

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))


url='https://www.rottentomatoes.com/m/exodus_gods_and_kings/reviews'
scrape(driver,url)