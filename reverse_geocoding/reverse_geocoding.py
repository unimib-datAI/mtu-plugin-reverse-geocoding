# THE NAME OF THE FILE (transform.py) MUST MATCH THE 'entry_file' entry in config.json
import os
import json
import requests

# READ THE COLUMN FROM input.json. the file contains the column in this format:
# {"original_column": ['cell-1', 'cell-2', ..., 'cell-n']}
file_path = f"{os.path.dirname(os.path.realpath(__file__))}/input.json"
file_open = open(file_path, encoding="utf-8")
data: dict[str, list[str]] = json.load(file_open)

# Updated Column
new_column = []
###


def get_request(lat: str, lon: str):
    """Create Request for Geocoordinates"""
    return f"""https://nominatim.openstreetmap.org/reverse.php?lat={lat}&lon={lon}&zoom=17&format=json"""


# HERE GOES YOUR PLUGIN CODE
cells = data["original_column"]
for cell in cells:
    lat, lon = cell.split(",")
    x = requests.get(
        get_request(lat.strip(), lon.strip()))
    if x.status_code == 200:
        response = x.json()
        if "error" in response:
            new_column.append("UNDEFINED STREET")
        else:
            new_column.append(response["display_name"])
    else:
        new_column.append("UNDEFINED STREET")
###

# WRITE COLUMN TO JSON FILE, THE NAME MUST MATCH THE 'output' entry in config.json
NAME_OF_THE_OUTPUT_FILE: str = "transform.json"
with open(f"{os.path.dirname(os.path.realpath(__file__))}/output/{NAME_OF_THE_OUTPUT_FILE}", 'w', encoding="utf-8") as f:
    json.dump({"new_column": new_column}, f)
