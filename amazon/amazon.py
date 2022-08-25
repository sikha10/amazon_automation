import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from amazon.amazon_report import AmazonReport
from prettytable import PrettyTable


class Amazon(webdriver.Chrome):
    def __init__(self, teardown=False, driver='D:\selenium chromedriver\chromedriver.exe'):
        super(Amazon, self).__init__()
        self.driver = driver
        self.teardown = teardown
        self.set_window_position(2000, 0)
        self.maximize_window()
        self.implicitly_wait(10)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def first_page(self):
        self.get('https://www.amazon.com/ref=nav_logo')

    def search_product(self, product: str):
        search = self.find_element(By.ID, "twotabsearchtextbox")
        search.clear()
        search.send_keys(product)
        search_button = self.find_element(By.ID, "nav-search-submit-text")
        search_button.click()

    def filter_featured(self):
        filter_button = self.find_element(By.ID, "a-autoid-0")
        filter_button.click()
        featured = self.find_element(By.CSS_SELECTOR, 'li[aria-labelledby="s-result-sort-select_0"]')
        featured.click()

    def filter_low_to_high(self):
        filter_button = self.find_element(By.ID, "a-autoid-0")
        filter_button.click()
        LowtoHigh = self.find_element(By.CSS_SELECTOR, 'li[aria-labelledby="s-result-sort-select_1"]')
        LowtoHigh.click()

    def filter_high_to_low(self):
        filter_button = self.find_element(By.ID, "a-autoid-0")
        filter_button.click()
        high_to_low = self.find_element(By.CSS_SELECTOR, 'li[aria-labelledby="s-result-sort-select_2"]')
        high_to_low.click()

    def filter_avg_customer_review(self):
        filter_button = self.find_element(By.ID, "a-autoid-0")
        filter_button.click()
        avg_customer_review = self.find_element(By.CSS_SELECTOR, 'li[aria-labelledby="s-result-sort-select_3"]')
        avg_customer_review.click()

    def filter_newest_arrivals(self):
        filter_button = self.find_element(By.ID, "a-autoid-0")
        filter_button.click()
        newest_arrivals = self.find_element(By.CSS_SELECTOR, 'li[aria-labelledby="s-result-sort-select_4"]')
        newest_arrivals.click()

    def brand_filter(self):
        brands = self.find_element(By.ID, "brandsRefinements")
        elements = brands.find_elements(By.CLASS_NAME, "a-spacing-micro")
        brand_list = []
        for b in elements:
            br = b.get_attribute('aria-label')
            brand_list.append(br)
        print(brand_list)

    def choose_brand(self, *brand_name):  # gasasworebelia or an met brends ver poulobs
        for names in brand_name:
            brands = self.find_element(By.ID, "brandsRefinements")
            elements = brands.find_elements(By.CLASS_NAME, "a-spacing-micro")
            for brand in elements:
                brand_attributes = brand.get_attribute('aria-label')
                if brand_attributes == names:
                    elem = self.find_element(By.ID, f'p_89/{names}')
                    link = elem.find_element(By.CSS_SELECTOR, 'a[class="a-link-normal s-navigation-item"]')
                    link.click()

    # def report(self):  # satadarigo
    #     results = self.find_element(By.CSS_SELECTOR, 'div[class="s-main-slot s-result-list s-search-results sg-row"]')
    #     report = AmazonReport(results)
    #     report.pull_attributes()

    def report(self):
        self.implicitly_wait(1)
        results = self.find_element(By.CSS_SELECTOR, 'div[class="s-main-slot s-result-list s-search-results sg-row"]')
        boxes = results.find_elements(By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
        price_boxes = results.find_elements(By.CSS_SELECTOR, 'div[class="a-section a-spacing-small a-spacing-top-small"]')
        collection = []
        stars = results.find_elements(By.CSS_SELECTOR, 'span[class="a-icon-alt"]')
        for star, name, prices in zip(stars, boxes, price_boxes):
            names = name.find_element(By.CSS_SELECTOR, 'span[class="a-size-medium a-color-base a-text-normal"]')
            title = names.get_attribute('innerHTML')
            rating = star.get_attribute('innerHTML')
            try:
                price_box = prices.find_element(
                By.CSS_SELECTOR, 'span[class="a-price"]')
                price = price_box.find_element(
                    By.CSS_SELECTOR, 'span[class="a-offscreen"]').get_attribute('innerHTML')
                collection.append([title, rating, price])
            except:
                collection.append([title, rating, 'none'])
        table = PrettyTable(
            field_names=['Name', 'Rating', 'Price']
        )
        table.add_rows(collection)
        print(table)

    def print_last_page(self):
        self.implicitly_wait(3)
        page_parent_element = self.find_element(By.CSS_SELECTOR, 'div[class="s-widget-container s-spacing-medium s-widget-container-height-medium celwidget slot=MAIN template=PAGINATION widgetId=pagination-button"]')
        try:
            last_page = page_parent_element.find_element(
            By.CSS_SELECTOR, 'span[class="s-pagination-item s-pagination-disabled"]').get_attribute('innerHTML')
        except:
            last_page = page_parent_element.find_element(
                By.CSS_SELECTOR, 'a[class="s-pagination-item s-pagination-button"]').get_attribute('innerHTML')
        print(f'last page is: {last_page}')

    def go_to_page(self, pages: int = 1):
        page_parent_element = self.find_element(By.CSS_SELECTOR, 'div[class="s-widget-container s-spacing-medium s-widget-container-height-medium celwidget slot=MAIN template=PAGINATION widgetId=pagination-button"]')
        first_page = self.find_element(By.CSS_SELECTOR, 'span[class="s-pagination-item s-pagination-selected"]')
        first_page_attribute = first_page.get_attribute('innerHTML')
        while int(first_page_attribute) != 1:
            previous = self.find_element(By.CSS_SELECTOR, 'a[class="s-pagination-item s-pagination-previous s-pagination-button s-pagination-separator"]')
            previous.click()
            first_page = self.find_element(By.CSS_SELECTOR, 'span[class="s-pagination-item s-pagination-selected"]')
            first_page_attribute = first_page.get_attribute('innerHTML')

        # find next button and click until it will become page variable number
        pages_attribute = self.find_element(
            By.CSS_SELECTOR, 'span[class="s-pagination-item s-pagination-selected"]').get_attribute('innerHTML')
        self.report()
        while int(pages_attribute) != pages:
            next_button = self.find_element(By.CSS_SELECTOR, 'a[class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
            next_button.click()
            pages_attribute = self.find_element(
                By.CSS_SELECTOR, 'span[class="s-pagination-item s-pagination-selected"]').get_attribute('innerHTML')
            self.report()
            time.sleep(3)

