import json
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import os

from get_txn_data import generate_and_save_txn_data
from get_node_data import generate_and_save_node_data

def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    
    with open(os.path.join(script_dir, 'node_locations.json'), 'r') as f:
        node_locations = json.load(f)

    with open(os.path.join(script_dir, 'transaction_data.json'), 'r') as f:
        transaction_data = json.load(f)
        
    return node_locations, transaction_data

def extract_node_coordinates(node_locations):
    return {int(k.replace("node", "")): (v['latitude'], v['longitude']) 
            for k, v in node_locations.items()}

def calculate_relative_distances(transaction_data):
    newest_relative_distances = {}
    for transaction_id, transaction in transaction_data.items():
        timestamps = {int(node_data.replace("node", "")): time 
                      for data in transaction for node_data, time in data.items()}
        first_node_id = min(timestamps, key=timestamps.get)
        newest_relative_distances[transaction_id] = {
            node_id: np.abs(time - timestamps[first_node_id]) 
            for node_id, time in timestamps.items()
        }
    return newest_relative_distances

def residuals_adjusted(params, node_coords, relative_dists):
    x, y, k = params
    residuals = []
    for node_id, d_i in relative_dists.items():
        x_i, y_i = node_coords[node_id]
        residuals.append((x - x_i)**2 + (y - y_i)**2 - (k * d_i)**2)
    return residuals

def estimate_transaction_origins(newest_relative_distances, node_coordinates):
    initial_guess = (0, 0, 1)
    newest_estimated_origins = {}
    for transaction_id, relative_dists in newest_relative_distances.items():
        result = least_squares(residuals_adjusted, initial_guess, 
                               args=(node_coordinates, relative_dists))
        x_est, y_est, _ = result.x
        newest_estimated_origins[transaction_id] = (x_est, y_est)
    return newest_estimated_origins

def visualize_estimated_origins(newest_estimated_origins, node_coordinates):
    newest_origin_lats, newest_origin_lons = zip(*newest_estimated_origins.values())
    newest_node_lats, newest_node_lons = zip(*node_coordinates.values())
    plt.figure(figsize=(10, 6))
    plt.scatter(newest_origin_lons, newest_origin_lats, color='blue', s=15, label='Estimated Origins')
    plt.scatter(newest_node_lons, newest_node_lats, color='red', s=50, marker='s', label='Nodes')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Scatter Plot of Estimated Transaction Origins and Node Locations')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Number of sample transactions to create
    num_transactions = 20
    
    # Number of sample nodes to create
    num_nodes = 5
    
    # Generate fake node data
    generate_and_save_node_data(num_nodes, 'node_locations.json')
    
    # Generate fake transaction data
    generate_and_save_txn_data(num_transactions, num_nodes, 'transaction_data.json')
    
    # Load data
    node_locations, transaction_data = load_data()

    # Get geographical coordinates of nodes from the generated node location data.
    node_coordinates = extract_node_coordinates(node_locations)
    
    # Compute the relative distances between nodes and transactions based on the 
    # difference in their respective timestamp data.
    newest_relative_distances = calculate_relative_distances(transaction_data)
    
    # Estimate the geographical origins of transactions using multilateration, based on 
    # relative distances and node coordinates.
    newest_estimated_origins = estimate_transaction_origins(newest_relative_distances, node_coordinates)
    
    # Create a scatter plot to visualize the estimated transaction origins and node 
    # locations on a coordinate plane.
    visualize_estimated_origins(newest_estimated_origins, node_coordinates)
    