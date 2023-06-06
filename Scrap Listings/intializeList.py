import re
import shutil

# Read the areas from the 'areas.txt' file
with open('areas.txt', 'r') as f:
    areas = f.read().splitlines()

formatted_areas = []
for area in areas:
    # Replace spaces with hyphens
    area = area.lower().replace(' ', '-')

    # Replace multiple hyphens with a single hyphen
    area = re.sub('-+', '-', area)

    # Replace special characters
    area = area.replace('(', '').replace(')', '').replace('.', '').replace('/', '-')

    # Replace all numbers with hyphens and numbers
    area = re.sub(r'\d+', lambda x: '-' + x.group(), area)

    formatted_areas.append(area)

# Filter out any empty areas
allareas = list(filter(None, formatted_areas))

newlist = []
for areas in allareas:
    # Create a list with area and type (rent/sale) combinations
    newlist.append([areas, 'rent'])
    newlist.append([areas, 'sale'])

import json

# Save the new list as a JSON file named 'areas.json'
with open('areas.json', 'w') as f:
    json.dump(newlist, f)

# Create a copy of the 'areas.json' file named 'areas_copy.json'
shutil.copy("areas.json", "areas_copy.json")
