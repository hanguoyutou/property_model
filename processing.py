import numpy as np
from geocoder import arcgis

def split_by_space(column):
    '''
    split by '\xa0' for location pre-processing
    '''
    area = []
    building = []
    try:
        for col in column:
            split = col.split('\xa0')
            area.append(split[0])
            building.append(split[1])
    finally:
        area = np.array(area).T
        building = np.array(building).T
    return area,building

def split_by_dash(column):
    '''
    split year and month by '-'
    '''
    year = []
    month = []
    try:
        for col in column:
            split = col.split('-')
            year.append(split[0])
            month.append(split[1])
    finally:
        year = np.array(year).T
        month = np.array(month).T
    return year,month

def data_process(raw_data):
    y, m = split_by_dash(raw_data[:,0])
    a, b = split_by_space(raw_data[:,1])
    raw_data = np.insert(raw_data,2,b,axis=1)
    raw_data = np.insert(raw_data,2,a,axis=1)
    raw_data = np.delete(raw_data,-2,1)
    raw_data = np.delete(raw_data,-2,1)
    raw_data = np.insert(raw_data,1,y,axis=1)
    raw_data = np.insert(raw_data, 2, m, axis=1)
    data = raw_data.copy()
    return data     #data是一个16行12列的ndarray  #['Time','Year','Month',
    # 'Location','District','Building','Floor','Unit','Area(ft^2)','Price(M)','Price/ft^2','Reference']

def long_n_lat(address):
    '''
    transfer a address from string to (long,lat)
    '''
    location = str(address)
    g = arcgis(location)
    long = g.json['lng']
    lati = g.json['lat']
    lng = round(long,4)
    lat = round(lati,4)
    return lng, lat

def gis_data():
    '''
    transfer location to longitude and latitude value
    '''
