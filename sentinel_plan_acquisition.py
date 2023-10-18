"""
Tom Kenda (UCLouvain), Octobre 2023, PHENET Project

This script is used to get the date and time when Sentinels will fly over a given zone.
After this, an .ics file is created to be imported in a calendar application (e.g. Google Calendar)
For more info see : https://api.spectator.earth/?language=Python#spectator-api-docs and
https://icspy.readthedocs.io/en/stable/api.html#calendar

Available satellites are :
Sentinel-1A, Sentinel-1B, Sentinel-2A, Sentinel-2B, Sentinel-3A, Landsat-8
"""
# set up
import requests
import geopandas as gpd
import pandas as pd
from ics import Calendar, Event


api_key    = 'bCWPiwyNrWjrXkFQERr3a8'
satellites = 'Sentinel-2A,Sentinel-2B,Sentinel-1B'
days_after = 15 # number of days after the request to get the data

#open shapefile of the zone of interest - convert it to WGS84 - get the bounding box
vector_path  = '/export/homes/tkenda/DATA/Dataset_creation/'
bbox = gpd.read_file(f'{vector_path}lpis_interyear_20-22_b-10m_min-1ha_phenet_parcel.shp'
                     ).to_crs('EPSG:4326'
                              ).total_bounds

# bbox should be of the form bbox = '19.59,49.90,20.33,50.21' # xmin,ymin,xmax,ymax
# convert it to string
bbox = ','.join(map(str, bbox))

print(bbox)

# get the data
url = 'https://api.spectator.earth/overpass/?bbox={bbox}&satellites={satellites}&api_key={api_key}&days_after={days_after}'.format(
    bbox=bbox, satellites=satellites, api_key=api_key, days_after=days_after)
response = requests.get(url)
data = response.json()

# for each overpasses, get the 'date', 'satellite' and 'acquisition' data
df = pd.DataFrame(columns=['id' ,'date', 'satellite', 'acquisition'])
# set the length of the dataframe to the number of overpasses
df = df.reindex(range(len(data['overpasses'])))

# loop over the overpasses to store the data in the dataframe
for i, overpass in enumerate(data['overpasses']):
  df.iloc[i] = [overpass['id'],
                overpass['date'], 
                overpass['satellite'], 
                overpass['footprints']['features'][0]['properties']['acquisition']
                ]

# keep row where acquisition is True
df = df[df['acquisition']==True]
print(df)

# create a .ics file with the dates and the title of the event it the name of the sattelite
c = Calendar()

for index, row in df.iterrows():
    e = Event()
    e.name        = row['satellite']
    e.begin       = row['date']
    e.description = str(row)
    e.duration    = {'minutes': 30}
    e.transparent = True # set availability to 'free'
    e.categories  = ['Satellite']
    c.events.add(e)

# all the events are stored in the calendar c as .ics file   
with open(f'/export/homes/tkenda/DATA/sentinel_acquision_cal.ics', 'w') as f:
    f.write(str(c))
