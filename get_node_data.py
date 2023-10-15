import json
import random
import os

def generate_and_save_node_data(n, file_name):
    """
    Generate n random geographic coordinates, ensuring that longitudes are within 
    [-180, 180], and save them to a JSON file.
    
    Parameters:
        n (int): The number of coordinates to generate.
        file_name (str): The name of the JSON file to save the data.
    """
    locations = []
    step_size = 360 / n

    for i in range(n):
        lon = random.uniform(i * step_size, (i + 1) * step_size) % 360
        lon = lon if lon <= 180 else lon - 360
        lat = random.uniform(-90, 90)
        locations.append((lat, lon))
    
    locations_dict = {f"node{i+1}": {"latitude": lat, "longitude": lon} 
                      for i, (lat, lon) in enumerate(locations)}

    script_dir = os.path.dirname(os.path.abspath(__file__))  
    file_path = os.path.join(script_dir, file_name)
    
    # Check if the file exists and delete it if it does
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(locations_dict, f, ensure_ascii=False, indent=4)
