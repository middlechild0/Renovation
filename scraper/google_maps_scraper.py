
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class GoogleMapsScraper:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=chrome_options)

    def search_barbershops(self, location, max_results=20):
        url = f"https://www.google.com/maps/search/barbershop+in+{location}"
        self.driver.get(url)
        time.sleep(5)
        results = []
        cards = self.driver.find_elements(By.CSS_SELECTOR, '[role="article"]')
        for card in cards[:max_results]:
            try:
                name = card.text
                card.click()
                time.sleep(2)
                website = ''
                rating = ''
                try:
                    website = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Website').get_attribute('href')
                except:
                    website = ''
                try:
                    rating = self.driver.find_element(By.CSS_SELECTOR, 'span[aria-label*="stars"]').text
                except:
                    rating = ''
                results.append({
                    'name': name,
                    'website': website,
                    'rating': rating,
                    'location': location
                })
            except:
                continue
        return results

    def close(self):
        self.driver.quit()
