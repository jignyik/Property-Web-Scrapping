# Property Listings Scraper

This project consists of three Python scripts that work together to scrape property listings from a website. The scripts are described below:

## 1. `scrapListings.py`

This script utilizes the Selenium library to scrape property listings from a website. It iterates through a list of areas and determines whether to search for properties for sale or rent. It performs the following tasks:

- Imports necessary libraries and defines helper functions.
- Sets up a headless Firefox browser using Selenium.
- Iterates through the list of areas and sale/rent types.
- Checks if the CSV file and checkpoint file exist for each area.
- Enters the search parameters into the website and retrieves the property listings.
- Handles cases of Captcha detection, errors, and the end of pages.
- Extracts relevant information from the listings and saves it to a CSV file.
- Updates the checkpoint file and moves to the next area.

## 2. `csv_save.py`

This script contains utility functions for handling CSV files, JSON files, and checking internet connectivity. The functions are described as follows:

- `save_into_csv`: Saves property listing information into a CSV file.
- `load_data_from_json`: Loads data from a JSON file.
- `save_data_to_json`: Saves data to a JSON file.
- `append_to_csv`: Appends data to a CSV file.
- `check_csv_file`: Checks if the CSV file exists and creates it if not.
- `check_page_file`: Checks if the JSON file for checkpoints exists and creates it if not.
- `load_checkpoint`: Loads the checkpoint (page number) from a JSON file.
- `save_checkpoint`: Saves the checkpoint (page number) to a JSON file.
- `check_internet`: Checks if there is an active internet connection.

These utility functions help in managing the CSV files, JSON files, and handling internet connectivity for the main script.

## 3. `initializeList.py`

This script reads a list of areas from a text file, formats them, and saves the formatted areas as a JSON file. It performs the following tasks:

- Reads the areas from the 'areas.txt' file.
- Formats each area by replacing spaces with hyphens, removing special characters, and replacing numbers with hyphens and numbers.
- Filters out any empty areas from the formatted list.
- Creates a new list with area and type (rent/sale) combinations.
- Saves the new list as a JSON file named 'areas.json'.
- Creates a copy of the 'areas.json' file named 'areas_copy.json'.

## Dependencies

- Selenium: version 3.x
- Mozilla Firefox browser
- geckodriver: compatible with your Firefox version
- Python: version 3.x

## Usage

1. Install the required dependencies.
2. Download the geckodriver and place it in the project directory.
3. Prepare the 'areas.txt' file with the desired areas to search for property listings.
4. Run `initializeList.py` to format the areas and generate the 'areas.json' file.
5. Execute `scrapListings.py` to start scraping property listings based on the areas and types specified in 'areas.json'.
6. The script will create CSV files with the scraped data for each area and type combination.
7. Check the output directory for the generated CSV files.

Please ensure that you comply with the terms of service of the website you are scraping and respect any applicable legal and ethical considerations while using this script.
