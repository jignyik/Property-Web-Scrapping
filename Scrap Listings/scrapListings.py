import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from csv_save import save_into_csv, load_data_from_json, save_data_to_json, check_csv_file, check_page_file, load_checkpoint, save_checkpoint, check_internet
from selenium.common.exceptions import NoSuchElementException

# File paths
area_json_file = "areas_copy.json"
page_file = 'checkpoints.json'

# Load the search areas from a JSON file
allareas = load_data_from_json(area_json_file)

# Configure Firefox options
options = Options()
options.headless = True
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Iterate over each search area and sale/rent type
for i, data in enumerate(allareas):
    searcharea = data[0]
    sale_or_rent = data[1]

    # Check if the CSV file for saving the data exists
    csv_file_name = str("test/"+searcharea+"_"+sale_or_rent+".csv")
    csvList = ['sale_or_rent', 'Search Area', 'Time', 'Price', 'Price per sq. ft.', 'Location', 'Extra Location',
                             'Type and Features', 'Bedrooms', 'Bathrooms', 'Parking']
    check_csv_file(csv_file_name, csvList)

    # Check if the checkpoint file exists
    check_page_file(page_file)

    # Start an infinite loop to retry in case of errors
    # This loop breaks when all pages for a particular area and sale/rent type are finished
    while True:
        # Check internet connection
        if not check_internet():
            print("Internet connection is not active, retrying in 30 seconds...")
            time.sleep(30)
            continue

        # Load the checkpoint page number
        page = load_checkpoint(page_file)

        # Create a Firefox webdriver instance
        driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options)

        # Construct the URL for the search page
        # Change 'selangor' to states that you want to search
        # Check the url on Iproperty
        link = "https://www.iproperty.com.my/{}/selangor/{}/all-residential/?page={}".format(sale_or_rent, searcharea, page)
        print(link)
        driver.get(link)

        # Try to detect if there is a Captcha
        try:
            captcha = driver.find_element_by_xpath("//div[contains(@class, 'error txtC')]")
            # Captcha found
            print("Captcha detected, retrying...")

            # Save the checkpoint so we can continue on this page and close the browser
            save_checkpoint(page_file, page)
            driver.quit()
            continue

        except NoSuchElementException:
            pass

        # Handle exceptions and retry if any error occurs
        try:
            elements = driver.find_elements_by_xpath("//li[contains(@class, 'ListingsListstyle__ListingListItemWrapper')]")

            # Find the keyword indicating the end of pages (no more next page)
            # Typically, when an error occurs here, it indicates a captcha
            endofpage = driver.find_element_by_xpath("//*[contains(text(), 'Make sure all spelling is correct')]")
        except:
            print('Some error occurred, retrying...')
            driver.quit()
            continue

        # Remove 'From x price to y price' advertisements and auction-related listings
        # Save the remaining listings into the CSV file
        for elem in elements:
            if 'From' not in elem.text:
                if 'Auction' not in elem.text:
                    try:
                        save_into_csv(elem.text, sale_or_rent, searcharea, csv_file_name)
                    except:
                        pass

        # No more pages, navigate to the next area
        if endofpage.text != '':
            driver.quit()

            # Delete the current area that it is searching from the list
            area_list = load_data_from_json(area_json_file)
            del area_list[0]
            save_data_to_json(area_list, area_json_file)

            # Refresh the checkpoint to page 1 for the new area
            save_checkpoint(page_file, 1)
            break

        # Close the browser and navigate to the next page
        else:
            driver.quit()
            # Save the checkpoint with page+1
            save_checkpoint(page_file, page + 1)
