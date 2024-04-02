import scrapy
import json

class PracujSpider(scrapy.Spider):
    name = 'pracuj_spider'
    allowed_domains = ['pracuj.pl']
    start_urls = ['https://www.pracuj.pl/praca/ksiegowy;kw/gdynia;wp?rd=30']

    def parse(self, response):
        # Extract the JSON data from the <script> tag
        script_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        
        # Parse the JSON data
        json_data = json.loads(script_data)
        
        # Extract the job listings from the JSON data
        job_listings = json_data['props']['pageProps']['data']['jobOffers']['groupedOffers']
        
        for job in job_listings:
            yield {
                'title': job['jobTitle'],
                'company': job['companyName'],
                'lastPublicated': job.get('lastPublicated', ''),
                'expirationDate': job.get('expirationDate', ''),
                'salaryDisplayText': job.get('salaryDisplayText', ''),
                'jobDescription': job.get('jobDescription', ''),
                'offerAbsoluteUri': job.get('offerAbsoluteUri', ''),
                'displayWorkplace': job.get('displayWorkplace', ''),
                'positionLevels': job.get('positionLevels', []),
                'typesOfContract': job.get('typesOfContract', []),
                'workSchedules': job.get('workSchedules', []),
                'workModes': job.get('workModes', []),
                'primaryAttributes': job.get('primaryAttributes', [])
            }

        # Check if there is a next page
        next_page_url = response.css('a.pagination_bfwjnw0[data-test="link-pagination-next"]::attr(href)').get()
        if next_page_url:
            yield scrapy.Request(url=response.urljoin(next_page_url), callback=self.parse)