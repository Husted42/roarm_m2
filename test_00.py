import requests
import argparse
import json


def main():

    command = {"T":1051,"x":373.8055574,"y":287.1348881,"z":112.6639825,"b":0.655009796,"s":0.813009818,"e":0.859029241,"t":3.136990711,"torB":80,"torS":200,"torE":-116,"torH":0}
    json_command = json.dumps(command)
    ip_addr = '192.168.0.147'

    url = "http://" + ip_addr + "/js?json=" + json_command
    print(f"Sending command to {url}")
    response = requests.get(url)
    content = response.text
    print(content)


if __name__ == "__main__":
    main()