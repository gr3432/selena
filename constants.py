import json

with open("constants.json") as f:
    data = json.load(f)
    webdriver_edge_path = data["webdriver_edge_path"]