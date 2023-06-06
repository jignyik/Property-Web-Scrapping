from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from chartExtract import extract_data_chart
import math
import json
import shutil

# Set up headless Firefox browser options
options = Options()
options.headless = True
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Create a new instance of the Firefox browser
driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options)

# Define the URL to scrape
link = "https://www.iproperty.com.my/transaction-price/residential/kuala-lumpur-mysta_26459/?page=1#location-table-header"

# Open the URL in the browser
driver.get(link)

# Find the number of results from the web page
num_of_results = driver.find_element_by_xpath("//p[contains(@class, 'TransactionTablestyle__TableSubHeader')]")
num_of_results = num_of_results.text
num_of_results = int(num_of_results.split()[0])

# Calculate the number of pages based on the number of results
num_of_pages = math.ceil(num_of_results/10)

# Close the browser
driver.quit()

# Initialize an empty list to store the data
data = []

# Iterate over the pages
for i in range(1, num_of_pages):
    print("{} / {} pages".format(i, num_of_pages))

    # Create a new instance of the Firefox browser for each page
    driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options)

    # Construct the URL for the current page
    link = "https://www.iproperty.com.my/transaction-price/residential/kuala-lumpur-mysta_26459/?page={}#location-table-header".format(i)

    # Open the current page in the browser
    driver.get(link)

    # Find the hyperlinks on the page
    hyperlinks = driver.find_elements_by_xpath("//*[contains(@class, 'TransactionLocationTablestyle__Link')]")

    # Extract the text and link for each hyperlink and add it to the data list
    for hp in hyperlinks:
        link = hp.get_attribute('href')
        data.append([hp.text, link])
        print([hp.text, link])

    # Close the browser for the current page
    driver.quit()

# Save the data to a JSON file
with open('project_links.json', 'w') as f:
    json.dump(data, f, indent=4)

# Create a copy of the JSON file
shutil.copy("project_links.json", "project_links_copy.json")
