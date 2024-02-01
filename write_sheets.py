import pygsheets
import pandas as pd

df = pd.DataFrame() 

gc = pygsheets.authorize(service_file='creds.json')
sh = gc.open('apt_astana')
wks = sh[0]

df['name'] = ['d', 'dd']
df['price'] = [1,3]

df['name'].append('ddd')
df['price'].append(43)
wks.set_dataframe(df,(1,1))