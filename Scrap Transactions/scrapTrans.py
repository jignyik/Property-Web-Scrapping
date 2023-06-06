# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from chartExtract import extract_data_chart, load_data_from_json, save_data_to_json, append_to_csv, check_csv_file
import json
import requests

# Set Selenium options for headless browsing
options = Options()
options.headless = True
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Load the list of links to scrape from a JSON file
json_checkpoint_file = 'project_links_copy.json'
links_to_scrap = load_data_from_json(json_checkpoint_file)

# Set the CSV file name and the title row for the CSV file
csv_file_name = 'TransactionData.csv'
list_csv_title = ['Property Name', 'Features', 'month1', 'data1', 'month2', 'data2', 'month3', 'data3', 'month4', 'data4', 'month5', 'data5', 'month6', 'data6', 'month7', 'data7', 'month8', 'data8', 'month9', 'data9', 'month10', 'data10', 'month11', 'data11', 'month12', 'data12']

# Check if the CSV file exists and create it with the appropriate header if it doesn't
check_csv_file(csv_file_name, list_csv_title)

# Loop through the list of links to scrape
for counter, name_and_link in enumerate(links_to_scrap):
    start_time = time.time()

    # Retry until internet connection is active
    while True:
        # Define the URL to check
        url = "https://www.google.com"

        # Send a request to the URL
        response = requests.get(url)

        # Check the response code
        if response.status_code == 200:
            # Internet connection is active
            break
        else:
            print("Internet connection is not active, retrying in 30 seconds...")
            time.sleep(30)
            continue

    # Initialize the WebDriver
    driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options)
    name = name_and_link[0]
    link = name_and_link[1]
    driver.get(link)
    time.sleep(1)

    try:
        # Check if Captcha is detected
        captcha = driver.find_element_by_xpath("//div[contains(@class, 'error txtC')]")
        print('Captcha detected, retrying...')
        driver.quit()
        continue
    except:
        pass

    try:
        # Get address and type
        address_and_type_data = driver.find_element_by_xpath("//p[contains(@class, 'TransactionSearchAndFilterstyle__Subtitle')]")
        address_and_type = address_and_type_data.text

        # Get all x-axis values
        x_axis = []
        x_values = driver.find_elements_by_xpath("//div[contains(@class, 'my-transaction-chart__x-axis-title')]")
        for x in x_values:
            x_axis.append(x.text)

        # Get all y-axis values
        y_axis = []
        y_values = driver.find_elements_by_xpath("//div[contains(@class, 'my-transaction-chart__y-axis-label')]")
        for y in y_values:
            y_axis.append(y.text)

        # Find all <path> elements within the <g> element
        point_paths = driver.find_elements_by_xpath("//*[contains(@class, 'highcharts-point')]")

        # Get the height and width of the graph
        plotbackground = driver.find_element_by_xpath("//*[contains(@class, 'highcharts-plot-background')]")
        width = plotbackground.get_attribute('width')
        height = plotbackground.get_attribute('height')

    except:
        print('Some error occurred, retrying...')
        driver.quit()
        continue

    # Extract the x and y coordinates of each point from the 'd' attribute
    positions = []
    for path in point_paths:
        d = path.get_attribute("d")
        # Extract the x and y values from the 'd' attribute
        x, y = d.split()[1], d.split()[2]
        # Convert the string coordinates to floats
        x, y = float(x), float(y)
        # Add the position to the list
        positions.append([x, y])

    # Extract data from the chart
    data = extract_data_chart(x_axis, y_axis, int(height), positions)

    # Flatten the data list and add property name and address/type
    flattened_data = [item for sublist in data for item in sublist]
    data_list = [name, address_and_type]
    for i in flattened_data:
        data_list.append(i)
    print(data_list)
    
    # Append data to the CSV file
    append_to_csv(csv_file_name, data_list)

    # Update the list of links to scrape
    links_to_scrap = load_data_from_json(json_checkpoint_file)
    del links_to_scrap[0]
    save_data_to_json(links_to_scrap, json_checkpoint_file)

    driver.quit()
    end_time = time.time()
    time_taken = end_time - start_time
    print("Time Taken:", time_taken, "seconds")
    print("Progress: {} Left to Scrap".format(len(links_to_scrap)))
    print(" ")
