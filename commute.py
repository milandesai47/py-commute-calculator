import json
from datetime import datetime


with open('sample.json') as json_file:
  data = json.load(json_file)
  for p in data['locations']:
    dtm = p['timestampMs']
    dtm2 = int(dtm)
    dateandtime = datetime.fromtimestamp(dtm2/1000)
    print('Date Time : ')
    print(dateandtime)

    print(p['latitudeE7'] / 10 ** 7)
    print(p['longitudeE7'] / 10 ** 7)