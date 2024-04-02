import os
import scrapy
from PyPDF2 import PdfReader
import pandas as pd

class PdfSpider(scrapy.Spider):
    name = 'pdf_spider'
    allowed_domains = ['ulc.gov.pl']
    start_urls = ['https://www.ulc.gov.pl/en/market-regulation/statictics-and-analysis-of-air-transport-market/4119-statistics-freight-on-board']

    def parse(self, response):
        # Specify the folder path where the PDF files are located
        folder_path = 'None/full'

        # Iterate over the PDF files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(folder_path, filename)
                self.process_pdf(pdf_path)

    def process_pdf(self, pdf_path):
        # Extract text from the PDF file
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()

        # Split the text into lines
        lines = text.split('\n')

        # Find the start and end indices of the tabular data
        start_index = None
        end_index = None
        for i, line in enumerate(lines):
            if line.startswith('Airport'):
                start_index = i
            elif line.startswith('Total'):
                end_index = i + 1
                break

        if start_index is not None and end_index is not None:
            # Extract the tabular data
            tabular_data = lines[start_index:end_index]

            # Create a DataFrame from the tabular data
            df = pd.DataFrame([line.split() for line in tabular_data])

            # Set the column names
            df.columns = df.iloc[0]
            df = df[1:]

            # Export the DataFrame to CSV
            csv_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.csv'
            df.to_csv(csv_filename, index=False)