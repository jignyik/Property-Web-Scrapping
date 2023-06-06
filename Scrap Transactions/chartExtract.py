import datetime
import json
import csv
import os

# Sample data for testing
x_points = ['Mar 22', 'Apr 22', 'May 22', 'Jun 22', 'Jul 22', 'Aug 22', 'Sep 22', 'Oct 22', 'Nov 22', 'Dec 22']
y_points = ['0', '200', '400', '600', '800']
width = 1110
height = 237
points = [[55.0, 25.0], [277.0, 181.0], [1054.0, 178.0]]

def extract_data_chart(x_points, y_points, height, points):
    """
    Extracts data from a chart based on given x and y points.

    Args:
        x_points (list): List of x-axis values.
        y_points (list): List of y-axis values.
        height (int): Height of the chart.
        points (list): List of points with x and y coordinates.

    Returns:
        list: Extracted data from the chart.
    """

    # Sort the points based on the x-coordinate
    sorted_points = sorted(points, key=lambda x: x[0])

    # Predict x-coordinates for each point based on the first point
    predicted_x = [points[0][0] + 2*i*points[0][0] for i in range(0, len(x_points)+1)]

    # Initialize compiled_data with "N/A" values
    compiled_data = [["N/A", "N/A"] for _ in range(len(x_points))]

    # Find the closest predicted x-coordinate for each point and assign the corresponding x and y values
    for i in points:
        c = i[0]
        closest_index = min(range(len(predicted_x)), key=lambda i: abs(predicted_x[i] - c))
        compiled_data[closest_index] = [x_points[closest_index], i[1]]

    # Update x-values in compiled_data
    for o, i in enumerate(compiled_data):
        i[0] = x_points[o]

    # Remove entries with "N/A"
    compiled_data = [i for i in compiled_data if "N/A" not in i]

    # Convert y-values to the appropriate scale based on the height and y-axis range
    y_points = [float(element) for element in y_points]
    min_y = min(y_points)
    max_y = max(y_points)
    def get_y_value(y):
        y_inv = height-y
        return round((y_inv/height * (max_y - min_y) + min_y)*1.005)

    # Update y-values in compiled_data
    for i in compiled_data:
        i[1] = get_y_value(i[1])

    return compiled_data

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
        data (list): Data to be appended as a row in the CSV file.
    """
    with open(csv_file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def check_csv_file(csv_file_name, listTitle):
    """
    Check if a CSV file exists, and if not, create it with the given list of titles as the header row.

    Args:
        csv_file_name (str): Name of the CSV file.
        listTitle (list): List of titles for the header row.
    """
    if not os.path.exists(csv_file_name):
        with open(csv_file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(listTitle)

if __name__ == "__main__":
    # Test the extract_data_chart function
    print(extract_data_chart(x_points, y_points, height, points))
