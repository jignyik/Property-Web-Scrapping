import csv
import datetime
from datetime import datetime, timedelta
import re
import os
import requests
from requests.exceptions import ConnectionError
import json

def save_into_csv(output, sale_or_rent, search_area, csv_file_name):
    """
    Save property listing information into a CSV file.

    Args:
        output (str): Property listing information.
        sale_or_rent (str): Indicates if it's a sale or rent listing.
        search_area (str): Search area for the property.
        csv_file_name (str): Name of the CSV file to save the data.
    """
    lines = output.strip().split('\n')

    # Remove unwanted lines
    if 'LiveTour' in lines[3]:
        del lines[3]

    # Find the line with the price
    for i, l in enumerate(lines):
        if "RM" in l:
            priceline = i - 1

    def convert_date_format(date_string):
        """
        Convert the date format from the given string.

        Args:
            date_string (str): Date string to convert.

        Returns:
            str: Converted date string.
        """
        if 'today' in date_string:
            date_string = date_string.replace('today', datetime.now().strftime('%Y-%m-%d'))
        elif 'yesterday' in date_string:
            yesterday = datetime.now() - timedelta(days=1)
            date_string = date_string.replace('yesterday', yesterday.strftime('%Y-%m-%d'))
        else:
            try:
                date_string = datetime.strptime(date_string, 'Posted on %d %b %Y %I:%M %p').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                date_string = datetime.strptime(date_string, 'Posted on %d %b %Y').strftime('%Y-%m-%d ')

        if 'Posted' in date_string:
            date_string = date_string[7:]

        date_string = date_string.split(" ")[0]
        return date_string

    # Extract property information
    sale_or_rent = sale_or_rent
    search_area = search_area
    time = convert_date_format(lines[1])
    price = lines[priceline]
    price_per_sq_ft = lines[priceline+1]
    location = lines[priceline+2]
    extra_location = lines[priceline+3]
    type_and_features = lines[priceline+4]
    bedrooms = lines[priceline+5]
    bathrooms = lines[priceline+6]
    parking = lines[priceline+7]

    # Check for the presence of digits in bedrooms and parking
    digit_pattern = re.compile(r'\d{1,2}')
    match = [digit_pattern.search(i) for i in [bedrooms, parking]]
    if not match[0]:
        bedrooms = 0
    if not match[1]:
        parking = 0

    # Append the property information to the CSV file
    with open(csv_file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sale_or_rent, search_area, time, price, price_per_sq_ft, location, extra_location,
                         type_and_features, bedrooms, bathrooms, parking])

    print([sale_or_rent, search_area, time, price, price_per_sq_ft, location, extra_location,
           type_and_features, bedrooms, bathrooms, parking])

def load_data_from_json(file_path):
    """
    Load data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded data from the JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_data_to_json(data, file_path):
    """
    Save data to a JSON file.

    Args:
        data (dict): Data to be saved.
        file_path (str): Path to the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f)

def append_to_csv(csv_file_name, data):
    """
    Append data to a CSV file.

    Args:
        csv_file_name (str): Name of the CSV file.
        data (list): Data to be appended to the CSV file.
    """
    with open(csv_file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def check_csv_file(csv_file_name, listTitle):
    """
    Check if the CSV file exists and create it if not.

    Args:
        csv_file_name (str): Name of the CSV file.
        listTitle (list): List of column titles for the CSV file.
    """
    if not os.path.exists(csv_file_name):
        with open(csv_file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(listTitle)

def check_page_file(json_file_name):
    """
    Check if the JSON file exists and create it if not.

    Args:
        json_file_name (str): Name of the JSON file.
    """
    if not os.path.exists(json_file_name):
        data = {
            "page": 1
        }
        with open(json_file_name, 'w') as f:
            json.dump(data, f, indent=4)

def load_checkpoint(json_file_name):
    """
    Load the checkpoint from a JSON file.

    Args:
        json_file_name (str): Name of the JSON file.

    Returns:
        int: Page number from the checkpoint.
    """
    with open(json_file_name) as f:
        checkpoints = json.load(f)
    page = checkpoints['page']
    return page

def save_checkpoint(json_file_name, page):
    """
    Save the checkpoint to a JSON file.

    Args:
        json_file_name (str): Name of the JSON file.
        page (int): Page number to be saved in the checkpoint.
    """
    data = {
        "page": page
    }
    with open(json_file_name, 'w') as f:
        json.dump(data, f, indent=4)

def check_internet():
    """
    Check if there is an active internet connection.

    Returns:
        bool: True if there is an active internet connection, False otherwise.
    """
    try:
        url = "https://www.google.com"
        response = requests.get(url)

        if response.status_code == 200:
            # Internet connection is active
            return True
        else:
            # No internet connection
            return False
    except ConnectionError:
        return False
