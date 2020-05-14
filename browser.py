from collections import deque
from pathlib import Path
import requests

import os
import sys

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

sites = {'bloomberg.com': bloomberg_com,
         'nytimes.com': nytimes_com}

history = deque()

storage = sys.argv[1]
Path(storage).mkdir(exist_ok=True)

while True:
    url = input()
    if url == 'exit':
        exit(0)
    parts = url.split('.')
    if len(parts) == 1:
        action = parts[0]
        if action in sites.keys():
            with open(storage + f"/{action}", 'r') as f:
                print(f.read())
            history.append(action)
        elif action == 'back':
            history.pop()
            with open(storage + f"/{history.pop()}", 'r') as f:
                print(f.read())
        else:
            print("Error: Not Found in local database...")

    elif len(parts) == 2 and url in sites:
        print(sites[url])
        history.append(parts[0])
        with open(storage + f"/{parts[0]}", 'w') as f:
            f.write(sites[url])

    else:
        print("Error: url not found")
