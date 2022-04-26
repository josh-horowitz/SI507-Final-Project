import csv
import json

with open('us-airports.csv','r') as fileObj:
    data = {}
    reader = csv.DictReader(fileObj, delimiter=',')
    for line in reader:
        data[line['ident']] = [line['latitude_deg'], line['longitude_deg']]

with open('us-airpots.json', 'w') as fileObj:
    json.dump(data, fileObj)