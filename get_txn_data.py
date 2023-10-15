import json
import random
import time
import os

def generate_random_timestamp():
    """
    Generate a random Unix timestamp in milliseconds.
    
    Returns:
        int: Unix timestamp (ms).
    """
    current_timestamp_sec = int(time.time())
    unix_epoch_timestamp_sec = 0
    random_timestamp_sec = random.randint(unix_epoch_timestamp_sec, current_timestamp_sec)
    random_timestamp_ms = random_timestamp_sec * 1000
    
    return random_timestamp_ms

def generate_and_save_txn_data(num_transactions, num_nodes, file_name):
    """
    Generate transaction and node data and save them to a JSON file.
    
    Args:
        num_transactions (int): Number of transactions to generate.
        num_nodes (int): Number of nodes per transaction.
        file_name (str): Name of the file to save data to.
    """
    tx_data = {}
    
    for i in range(num_transactions):
        tx_id = i + 1
        t_rand = generate_random_timestamp()
        
        nodes_data = []
        
        for j in range(num_nodes):
            t_node = t_rand + random.randint(-1000, 1000)
            nodes_data.append({
                f"node{j+1}": t_node,
            })
        
        tx_data[str(tx_id)] = nodes_data

    script_dir = os.path.dirname(os.path.abspath(__file__))  
    file_path = os.path.join(script_dir, file_name)
    
    # Check if the file exists and delete it if it does
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(tx_data, f, ensure_ascii=False, indent=4)
