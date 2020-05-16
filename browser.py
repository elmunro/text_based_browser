from collections import deque
from pathlib import Path
import requests

import os
import sys


def fetch_local_store(site_name: str):
    if site_name in sites.keys():
        with open(storage + f"/{site_name}", 'r') as f:
            print(f.read())
        history.append(site_name)
    else:
        print("Error: Not Found in local database...")


history = deque()

storage = sys.argv[1]
Path(storage).mkdir(exist_ok=True)
local_sites = {}
while True:
    input_str = input()
    if input_str == 'exit':
        exit(0)
    elif input_str == 'back':
        with open(storage + f"/{history.pop()}", 'r') as f:
            print(f.read())
    elif input_str in local_sites.keys():
        with open(storage+f"/{local_sites[input_str]}", 'r') as f :
            print(f.read())
    else:
        site_name = '.'.join(input_str.split('://')[-1].split('.')[:-1])
        clean_url = input_str.split('://')[-1]
        try:
            text = requests.get('https://' + clean_url).text
            history.append(site_name)
            local_sites[site_name] = clean_url
            print(text)
            with open(storage + f"/{clean_url}", 'w') as f:
                f.write(text)
        except requests.RequestException:
            print('Error, not found')
