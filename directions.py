import googlemaps
from pprint import pprint
from coordinates import gyms
import redis
import re
import pygsheets
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis()
gmaps = googlemaps.Client(key=os.getenv('GMAPS_TOKEN'))

data = {
    'link': [],
    'price': [],
    'rooms': [],
    'duration': [],
    'area': []
}

for key in r.scan_iter("areaN*"):
    key = key.decode("utf-8")
    gym_area = 0
    match = re.search(r'areaN_(\d+)', key) 
    if match:
        gym_area = int(match.group(1))#+1

    directions_result = gmaps.directions(gyms[gym_area],
                                        (float(r.hget(key, "lat").decode("utf-8")), 
                                        float(r.hget(key, "lon").decode("utf-8"))),
                                        mode="walking")
    
    data['link'].append("https://krisha.kz/a/show/"+re.sub('areaN_(\d+)_', '', key))
    data['price'].append(r.hget(key,"price").decode("utf-8"))  
    data['rooms'].append(r.hget(key,"rooms").decode("utf-8"))
    data['duration'].append(directions_result[0]['legs'][0]['duration']['value'])
    data['area'].append(gym_area)
    
df = pd.DataFrame(data) 

gc = pygsheets.authorize(service_file='creds.json')
sh = gc.open('apt_astana_v3')
wks = sh[0]
wks.set_dataframe(df,(1,1))

# directions_result = gmaps.directions((51.104743610762064, 71.39738780002877),
#                                         (51.113088881073644, 71.3975501277405),
#                                             mode="walking")
# for i in range(0, len(directions_result[0]['legs'])):
#     print(i)
#     print(directions_result[0]['legs'][i]['duration'])
