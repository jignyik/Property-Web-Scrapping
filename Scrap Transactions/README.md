# Property Transactions Scraper

This project consists of three Python scripts for scraping property transaction data and extracting relevant information from charts. Here's a brief overview of each script:

## 1. `scrapTrans.py`
   This script is responsible for scraping property transaction data from a website. It uses the Selenium library with Firefox WebDriver to navigate the website and extract the required information. The scraped data is then saved to a CSV file (`TransactionData.csv`) in a structured format.

## 2. `chartExtract.py`
   The `chartExtract.py` script contains functions for extracting data from charts. It provides a function called `extract_data_chart` that takes the x-axis labels, y-axis labels, height, and points of a chart as input. The function processes the data and returns a compiled data list with x and y values extracted from the chart.

## 3. `initializeProjects.py`
   The `initializeProjects.py` script initializes the scraping process. It retrieves property links and names from a website, stores them in a JSON file (`project_links.json`), and creates a backup copy (`project_links_copy.json`). The property links will be used by the `scrapTrans.py` script for scraping transaction data.

## Usage
1. Make sure you have Python 3 installed on your system.
2. Install the required dependencies by running the following command:


        pip install -r requirements.txt

3. Customize the scripts based on your specific requirements (e.g., update file paths, website URLs, etc.).
4. Run the `initializeProjects.py` script to retrieve and store property links.
5. Run the `scrapTrans.py` script to start scraping property transaction data and save it to the `TransactionData.csv` file.
6. Use the extracted data for further analysis or processing.

Feel free to modify the code and adapt it to your needs. Make sure to comply with the terms of service and policies of the website you are scraping.
