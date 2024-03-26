import scrapy
from pracuj_scraper.items import PracujScraperItem

class PracujSpider(scrapy.Spider):
    name = 'pracuj_spider'
    allowed_domains = ['pracuj.pl']
    start_urls = ['https://www.pracuj.pl/praca/ksiegowy;kw/gdynia;wp?rd=30']

    def __init__(self, *args, **kwargs):
        super(PracujSpider, self).__init__(*args, **kwargs)
        self.page_number = 1  # Initialize the page counter

    def parse(self, response):
        # Use the correct class selector with periods and no spaces
        for job in response.css('.tiles_b4e7s16.core_po9665q'):
            item = PracujScraperItem()
            # Uncomment and update the selectors below as needed
            # item['salary'] = job.css('li.offer__info--salary::text').get()
            # item['company'] = job.css('a.offer-details__company-name::text').get()
            # item['url'] = response.urljoin(job.css('a.offer-details__title-link::attr(href)').get())
            # item['localization'] = job.css('li.offer-labels__item--location::text').get()
            # item['date'] = job.css('span.offer-actions__date::text').get()
            
            # Update the selector for the title to match the correct class or structure
            item['title'] = job.css('h2::text').get()  # Assuming the title is within an <h2> tag
            
            yield item

        # Increment the page number
        self.page_number += 1
        next_page_url = f'https://www.pracuj.pl/praca/ksiegowy;kw/gdynia;wp?rd=30&pn={self.page_number}'

        # Check if there is a next page by looking for the presence of job offers on the page
        # This is a basic check and might need to be adjusted based on the actual page structure
        if response.css('.tiles_b4e7s16.core_po9665q'):
            yield response.follow(next_page_url, self.parse)
