#!/usr/bin/env python

"""Pull html pages"""

import os

import requests
from bs4 import BeautifulSoup as bs

offset = 20
page = 1
start = 0
response = 200

output_path = "/home/workboots/Datasets/IndiaCode/new/CentralActs/pages_html/"

for page, start in enumerate(range(0, 847, 20)):
    url = ("https://www.indiacode.nic.in/handle/123456789/1362/browse?"
           "type=shorttitle&sort_by=3&order=ASC&rpp=20&etal=-1&null=&"
           f"offset={start}")

    pull = requests.get(url)
    response = pull.status_code
    if response != 200:
        break

    soup = bs(pull.content)
    with open(os.path.join(output_path,
                           f"indiacode_central_acts_page_{page+1}.html"),
              'w') as f:
        f.write(str(soup.html))
