from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import scrapy
import time

class RocketJobsSpider(scrapy.Spider):
    name = 'rocketjobs'
    start_urls = ['https://rocketjobs.pl/wszystkie-lokalizacje/finanse']

    def scroll_and_extract(self, url):
        # Configure Selenium to run Chrome in headless mode
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")

        # Specify the path to chromedriver.exe (download and place it in your PATH)
        service = Service(executable_path=r"C:\Users\szymo\Downloads\chromedriver.exe")

        # Launch a headless browser session
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        # Scroll to the bottom of the page to load all jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for a moment to allow all jobs to load; adjust the delay as necessary
        time.sleep(5)

        # Extract the page source after scrolling
        content = driver.page_source
        driver.quit()
        return content

    def start_requests(self):
        # Override the start_requests to use Selenium for scrolling and extracting page content
        for url in self.start_urls:
            content = self.scroll_and_extract(url)
            # Convert the page content to a Scrapy response object
            response = scrapy.http.HtmlResponse(url=url, body=content, encoding='utf-8')

            # Extract job title, company, location, and URL for each job listing
            for offer in response.css('div.css-1tksz28'):
                yield {
                    'title': offer.css('h2.css-zxukvo::text').get(),
                    'company': offer.css('div.css-jx23jo span::text').get(),
                    'location': offer.css('div.css-1294shh div.css-1wao8p8::text').get(),
                    'url': offer.css('a.offer-list-offer_link::attr(href)').get()
                }