from RPA.Browser.Selenium import Selenium,WebDriverWait
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
        self.browser.headless = True
        try:
            self.browser.open_browser(url="https://www.aljazeera.com/")
        except:
            self.logger.error("There is an error connecting to aljazeera.com")
        self.logger.info("Aljazeera extractor initialized")
    def extractLatestNews(self,searchPhrase):
        self.searchPhrase = searchPhrase
        self.browser.click_element('class:icon--search')
        self.browser.input_text("class:search-bar__input",searchPhrase)
        self.browser.submit_form("class:search-bar__form")
        wait = WebDriverWait(self.browser.driver, timeout=5)
        try:
            wait.until(lambda d : len(self.browser.find_elements("class:search-summary__options-title"))!=0)
        except:
            self.logger.error("Could not fetch the latest news. Check")
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
        self.browser.click_element("tag:select option[value='date']")
        wait = WebDriverWait(self.browser, timeout=5)
        try:
            wait.until(lambda d : len(self.browser.find_elements("label.search-summary__options-title"))!=0)
        except:
            self.logger.info("")
            self.browser.close_browser()
            return
        wb = Workbook()
        ws = wb.active
        ws['A1'] = "Title"
        ws['B1'] = "Date" 
        ws['C1'] = "Description"
        ws['D1'] = "Picture Filename"
        ws['E1'] = "Count of Search Phrases"
        ws['F1'] = "Contains Amount of Money"
        counter = 2
        self.browser.get_text()
        for el in self.browser.find_elements(".search-result__list article"):
            title = el.get_text()("tag:span").text.replace('\xad','')
            date =  el.get_text()("tag:footer span[aria-hidden='true']")
            if len(date)==0:
                self.logger.info("There is no date for "+title+" title")
            # self.browser.
            description = el.find_element("class:gc__body-wrap p").text.replace('\xad','').replace('\"','')
            imageURL = el.find_element("tag:img").get_attribute("src")
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
                self.logger.info("Image Successfully Downloaded for "+title+" title")
            ws[f"A{counter}"] = title
            ws[f"B{counter}"] = "No Date" if len(date)==0 else date[0].text
            ws[f"C{counter}"] = description
            ws[f"D{counter}"] = imageName
            ws[f"E{counter}"] = countOfPhrase
            ws[f"F{counter}"] = str(containsCurrency)
            counter += 1
        wb.save(os.path.join("./",f'{int(datetime.now().timestamp())}.xlsx'))
        self.browser.quit()
            

al = AljazeeraExtractor()
al.extractLatestNews("science")