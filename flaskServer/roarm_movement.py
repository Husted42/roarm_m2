import os
from dotenv import load_dotenv, dotenv_values 


import requests
import argparse
import json
import time
import math
import pandas as pd

##### ----- Variables ----- #####
load_dotenv()  # Load env
ip_adress = os.getenv('IP')
base_path = os.getenv('DIR_PATH')
relative_path = f"events/test.csv"
csv_file = os.path.join(base_path, relative_path)

print(f"IP address: {ip_adress}")
print(f"CSV file path: {csv_file}")
 
##### ----- Functions ----- #####
def process_dataframe(csv_file = csv_file) -> tuple[pd.DataFrame, list]:
    
    """
    Read dataset and process it.
    """
    df = pd.read_csv(csv_file, header=0, sep=',', skipinitialspace=True)

    # Convert angles from degrees to radians
    df['elbow'] = df['elbow'].apply(lambda x: math.radians(x))
    df['hand'] = df['hand'].apply(lambda x: math.radians(x))
    df['shoulder'] = df['shoulder'].apply(lambda x: math.radians(x))
    df['base'] = df['base'].apply(lambda x: math.radians(x))

    # Extract how long the arm should wait after each command
    wait_times = df.pop('wait').tolist()

    # Add a 'T' column with a constant value
    df['T'] = 102

    return df, wait_times

def move_arm(command, ip_address):
    json_command = json.dumps(command)
    url = f"http://{ip_address}/js?json={json_command}"    
    response = requests.get(url)
    
    # Check if the response status code is 200 (OK)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return
    
    content = response.text

    return content

def main():
    """
    Main function to execute the arm movements.
    """
    df, wait_list = process_dataframe(csv_file)

    # Convert DataFrame to list of dictionaries
    list_commands = df.to_dict(orient='records')

    for i in range(0, len(list_commands)):
        print(f"Command {i+1}: {list_commands[i]}")
        move_arm(list_commands[i], ip_adress)  # Move arm
        time.sleep(wait_list[i])  # Wait between commands

if __name__ == "__main__":
    main()