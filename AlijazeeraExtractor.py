from RPA.Browser.Selenium import Selenium, WebDriverWait, By
from logging import getLogger, INFO
from urllib.request import urlopen
from os import path, mkdir
from re import search
from datetime import datetime
from openpyxl import Workbook


class AljazeeraExtractor:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.setLevel(INFO)
        self.log_file = f"aljazeera_{int(datetime.now().timestamp())}.log"
        self.browser = Selenium()
        self.browser.auto_close = False
        self.browser.open_available_browser(headless=True)
        self.search_phrase = None

    def extract_latest_news(self, search_phrase):
        self.search_phrase = search_phrase.lower()  # Preprocess search term
        self.browser.go_to("https://www.aljazeera.com/")
        try:
            self.search_news()
            self.extract_articles()
        except Exception as e:
            self.logger.error(f"Error: {e}")
        finally:
            self.browser.close_browser()

    def search_news(self):
        self.browser.click_element("class:icon--search")
        self.browser.input_text("class:search-bar__input", self.search_phrase)
        self.browser.submit_form("class:search-bar__form")
        wait = WebDriverWait(self.browser.driver, 20)
        wait.until(lambda d: len(d.find_elements("class:search-summary__options-title")) > 0)

    def extract_articles(self):
        articles = self.browser.find_elements("tag:article")
        if not articles:
            self.logger.info("No news found based on the search parameter")
            return

        self.browser.click_element("id:search-sort-option")
        self.browser.click_element('xpath://option[@value="date"]')
        wait = WebDriverWait(self.browser, 5)
        wait.until(lambda d: len(d.find_elements("class:search-summary__options-title")) > 0)

        wb = Workbook()
        sheet = wb.active
        sheet.append(["Title", "Date", "Description", "Picture Filename", "Count of Search Phrases", "Contains Amount of Money"])

        for article in articles:
            title = article.find_element(By.TAG_NAME, "span").text.strip()
            date_elements = article.find_elements(By.CLASS_NAME, "screen-reader-text")
            date = "No Date" if not date_elements else date_elements[0].text
            description = article.find_element(By.TAG_NAME, "p").text.strip().replace('"', '')
            image_url = article.find_element(By.TAG_NAME, "img").get_attribute("src")

            try:
                response = urlopen(image_url)
                image_data = response.read()
                image_name = "".join(title.split()[:3]).replace("|", "").replace(",", "")
                image_path = path.join("./", f"{image_name}.jpg")
                if not path.exists("./"):
                    mkdir("./")  # Create directory if it doesn't exist
                with open(image_path, "wb") as f:
                    f.write(image_data)
                self.logger.info(f"Image Successfully Downloaded for {title} title")
            except Exception as e:
                self.logger.error(f"Error downloading image for {title}: {e}")
                image_name = ""

            count_of_phrase = title.lower().count(self.search_phrase) + description.lower().count(self.search_phrase)
            currency_check = r"\$\d+\s*|\d+\s\$|\d+\sdollars|\d+\sUSD"
            contains_currency = search(currency_check, title) or search(currency_check, description)

            sheet.append([title, date, description, image_name, count_of_phrase, str(contains_currency)])

        wb.save("Aljazeera.xlsx")

al = AljazeeraExtractor()
al.extract_latest_news("science")