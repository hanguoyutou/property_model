import pandas as pd
from processing import long_n_lat
import numpy as np
import os

f = pd.read_csv('dataset.csv',na_values='NaN',index_col=False)
f = f.dropna()

# print(f['District'].drop_duplicates().__len__())  #62 - 1
# print(f['Building'].drop_duplicates().__len__())  #8302 - 1
# print(f['Location'].drop_duplicates().__len__())  #8535 - 1

location = f['Location'].drop_duplicates()

filename = 'gis_ref.csv'

try:
    for loc in location[:10]:        #remove index[:10] after testing
        lng, lat = long_n_lat(loc)
        gis = np.array((loc,lng,lat))
        df = pd.DataFrame([gis],columns=['Location','Longitude','Latitude'])
        if not os.path.isfile(filename):
            df.to_csv(filename,index=False)
        else:
            df.to_csv(filename, mode='a', header=False,index=False)
except Exception as e:
    print(e)