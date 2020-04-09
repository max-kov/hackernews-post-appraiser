import grequests
import requests
import json
import csv
import os

os.makedirs("data", exist_ok=True)

api_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
max_item = json.loads(requests.get("https://hacker-news.firebaseio.com/v0/maxitem.json").content)
entries_to_fetch = 100
cur_item = (max_item // entries_to_fetch) * entries_to_fetch
csv_columns = ['by', 'id', 'score', 'url', 'title', 'time', 'type']

while 1:
    f_name = "data/data_{}.csv".format(cur_item)

    if not os.path.exists(f_name):
        request_urls = (grequests.get(api_url.format(i), timeout=1) for i in
                        range(max_item - entries_to_fetch, max_item))
        responses = grequests.map(request_urls)

        with open(f_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns, extrasaction='ignore')
            writer.writeheader()
            for response in responses:
                if response is not None and response.status_code == requests.codes.ok:
                    data = json.loads(response.content)
                    if data is not None and data["type"] == "story":
                        writer.writerow(data)

    cur_item -= entries_to_fetch
    print("{} downloaded".format(cur_item))
