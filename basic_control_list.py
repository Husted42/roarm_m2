import requests
import argparse
import json
import time
import math

##### ----- Global Variables ----- #####
# TODO : Global variable - Update the IP address of your robot arm
ip_adress = '192.168.0.147'

# Command list
# TODO : Create a better format
list_commands = [
    # Starting position
    {"T":102,"base":0,"shoulder":0,"elbow": math.pi/2,"hand":math.pi * 0.5,"spd":0,"acc":10},
    
    {"T":102,"base":0,"shoulder":math.pi * 0.34,"elbow": (math.pi/2) * 0.3,"hand":math.pi * 0.5,"spd":0,"acc":10},
    {"T":102,"base":0,"shoulder":math.pi * 0.34,"elbow": (math.pi/2) * 0.3,"hand":math.pi,"spd":0,"acc":10},

    # Return to starting position
    {"T":102,"base":0,"shoulder":0,"elbow": math.pi/2,"hand":math.pi,"spd":0,"acc":10},
]

list_commands_1 = [
    {"T":102,"base":math.pi * 0.5,"shoulder": -math.pi * 0.5,"elbow": 0,"hand": 0,"spd":0,"acc":10},
]

def move_arm(command, ip_address):
    json_command = json.dumps(command)
    url = f"http://{ip_address}/js?json={json_command}"
    print(f"Sending command to {url}")
    
    response = requests.get(url)
    
    # Check if the response status code is 200 (OK)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return
    
    content = response.text

def main():
    for i in range(len(list_commands)):
        time.sleep(2)
        move_arm(list_commands[i], ip_adress)
    exit(0)


if __name__ == "__main__":
    main()