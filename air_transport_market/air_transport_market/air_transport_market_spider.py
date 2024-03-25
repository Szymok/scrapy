import scrapy
from air_transport_market.items import PdfFileItem

class PdfSpider(scrapy.Spider):
    name = 'pdf_spider'
    allowed_domains = ['ulc.gov.pl']
    start_urls = ['https://www.ulc.gov.pl/en/market-regulation/statictics-and-analysis-of-air-transport-market/4119-statistics-freight-on-board']

    def parse(self, response):
        # Extract PDF file URLs and yield PdfFileItem for each
        pdf_links = response.css('a::attr(href)').re(r'.*\.pdf$')
        for pdf_link in pdf_links:
            yield PdfFileItem(file_urls=[response.urljoin(pdf_link)])