from collections import deque
from pathlib import Path
import requests
from bs4 import BeautifulSoup

import os
import sys
from colorama import init, Fore, Style, Back


def print_text_from_html(html):
    init(autoreset=True)
    soup = BeautifulSoup(html, 'html.parser')
    text_tags = soup.find_all(['a', 'p', 'ul', 'li', 'ol'])
    for t in text_tags:
        if t.name == 'a':
            text = t.get_text()
            print(Fore.BLUE + text)
        else:
            print(t.get_text())


history = deque()
storage = sys.argv[1]
Path(storage).mkdir(exist_ok=True)
local_sites = {}

for file in os.listdir(storage):
    if os.path.isfile(os.path.join(storage, file)):
        name = '.'.join(file.split('.')[:-1])
        print("Found local: " + name)
        local_sites[name] = file


while True:
    input_str = input()
    if input_str == 'exit':
        exit(0)
    elif input_str == 'back':
        with open(storage + f"/{history.pop()}", 'rb') as f:
            print_text_from_html(f.read())
    elif input_str in local_sites.keys():
        with open(storage + f"/{local_sites[input_str]}", 'rb') as f:
            print_text_from_html(f.read())
    else:
        site_name = '.'.join(input_str.split('://')[-1].split('.')[:-1])
        clean_url = input_str.split('://')[-1]
        try:
            page = requests.get('https://' + clean_url)
            history.append(site_name)
            local_sites[site_name] = clean_url

            print_text_from_html(page.content)
            with open(storage + f"/{clean_url}", 'wb') as f:
                f.write(page.content)

        except requests.RequestException:
            print('Error, not found')
