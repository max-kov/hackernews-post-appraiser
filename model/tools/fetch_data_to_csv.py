import requests
import json
import csv

api_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
max_item = json.loads(requests.get("https://hacker-news.firebaseio.com/v0/maxitem.json").content)
csv_columns = ['by', 'id', 'score', 'url', 'title', 'time', 'type']
entries_to_fetch = 10

with open('data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns, extrasaction='ignore')
    writer.writeheader()
    for i in range(max_item-entries_to_fetch, max_item):
        data = json.loads(requests.get(api_url.format(i)).content)
        writer.writerow(data)
