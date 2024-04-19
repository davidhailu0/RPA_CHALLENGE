from RPA.Browser.Selenium import Selenium,WebDriverWait,By
import logging
import urllib.request
import os
import re
from  datetime import datetime
from openpyxl import Workbook

class AljazeeraExtractor:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        time = int(datetime.now().timestamp())
        logging.basicConfig(filename=f'aljazeera_{time}.log', level=logging.INFO)
        self.browser = Selenium()
        self.browser.auto_close = False
        self.browser.open_available_browser(headless=True)
        self.logger.info("Aljazeera extractor initialized")
    def extractLatestNews(self,searchPhrase):
        try:
            self.browser.go_to("https://www.aljazeera.com/")
        except:
            self.logger.error("There is an error connecting to aljazeera.com")
            self.browser.close_browser()
            return
        self.searchPhrase = searchPhrase
        self.browser.click_element('class:icon--search')
        self.browser.input_text("class:search-bar__input",searchPhrase)
        self.browser.submit_form("class:search-bar__form")
        wait = WebDriverWait(self.browser.driver, timeout=20)
        try:
            wait.until(lambda d : len(self.browser.find_elements("class:search-summary__options-title"))!=0)
        except:
            self.logger.error("Could not fetch the latest news.")
            self.browser.close_browser()
            return
        elem = self.browser.find_elements("class:search-results__no-results")
        if len(elem)!=0:
            self.logger.info("No news found based on the search parameter")
            self.browser.close_browser()
            return
        self.__extractHelper__()
    def __extractHelper__(self):
        self.browser.click_element("id:search-sort-option")
        self.browser.click_element('xpath://option[@value="date"]')
        wait = WebDriverWait(self.browser, timeout=5)
        try:
            wait.until(lambda d : len(self.browser.find_elements("class:search-summary__options-title"))!=0)
        except:
            self.logger.info("Unable to find the list of news")
            self.browser.close_browser()
            return
        wb = Workbook()
        sheet = wb.active
        sheet.append(["Title", "Date", "Description", "Picture Filename", "Count of Search Phrases", "Contains Amount of Money"])
        counter = 2
        for el in self.browser.find_elements("tag:article"):
            title = el.find_element(By.TAG_NAME,"span").text.replace('\xad','')
            date =  el.find_elements(By.CLASS_NAME,"screen-reader-text")
            if len(date)==0:
                self.logger.info(f"There is no date for ${title} title")
            description = el.find_element(By.TAG_NAME,"p").text.replace('\xad','').replace('\"','')
            imageURL = el.find_element(By.TAG_NAME,"img").get_attribute("src")
            response = urllib.request.urlopen(imageURL)
            imageData = response.read()
            imageName = "".join(title.split(' ')[:3]).replace("|","").replace(",","")
            countOfPhrase = title.lower().count(self.searchPhrase.lower())
            countOfPhrase += description.lower().count(self.searchPhrase.lower())
            currencyCheck = r"\$\d+\s*|\d+\s\$|\d+\sdollars|\d+\sUSD"
            containsCurrency = re.search(currencyCheck,title)!=None
            containsCurrency = containsCurrency or re.search(currencyCheck,description)!=None
            with open(os.path.join("./",f"{imageName}.jpg"),"wb") as f:
                f.write(imageData)
                self.logger.info(f"Image Successfully Downloaded for {title} title")
            date = "No Date" if len(date)==0 else date[0].text
            sheet.append([title, date, description, imageName, countOfPhrase, str(containsCurrency)])
            counter += 1
        wb.save("Aljazeera.xlsx")
        self.browser.close_browser()

if __name__ == "__main__":
    extractor = AljazeeraExtractor()
    extractor.extractLatestNews("science")
    
