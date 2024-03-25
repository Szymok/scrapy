import tabula
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

class PdfDataExtractionPipeline(FilesPipeline):

    def item_completed(self, results, item, info):
        # Check if the file was downloaded successfully
        if not results:
            raise DropItem("Item contains no files")

        # Path to the downloaded PDF file
        file_path = results[0][1]['path']
        # Extract tables from the PDF into pandas DataFrames
        tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
        # Do something with the extracted tables
        # For example, save them to CSV files or process them further

        return item