# satadarigod igive kodi amazon.py shi miweria report metodshi

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement


class AmazonReport:
    def __init__(self, boxes: WebElement):
        self.boxes = boxes
        self.names = self.pull_boxes()

    def pull_boxes(self):
        return self.boxes.find_elements(By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')

    def pull_attributes(self):
        collection = []
        stars = self.boxes.find_elements(By.CSS_SELECTOR, 'span[class="a-icon-alt"]')
        for star, name in zip(stars, self.names):
            names = name.find_element(By.CSS_SELECTOR, 'span[class="a-size-medium a-color-base a-text-normal"]')
            title = names.get_attribute('innerHTML')
            rating = star.get_attribute('innerHTML')
            collection.append([title, rating])
        print(collection)
