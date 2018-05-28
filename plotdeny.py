import requests
import sys
import re
import time
import pandas as pd
import plotly.offline as py

base_url = "https://www.iplocate.io/api/lookup/" #"http://ip-api.com/json/"

def get_location(ip):
    return requests.get(base_url+ip).json()

def get_all_locs(ip_list):
    count = 0
    data = []
    for ip in ip_list:
        count += 1
        if count > 1500:
            print("Too much ips! Limiting to 1500")
        else:
            data.append(get_location(ip))
            print("got location for ip: {}".format(ip))
    return data

def json_list_todf(json_list):
    return pd.DataFrame(json_list).transpose()

def map_reduce(json_list,by,new,keep):
    to_return = dict()
    for el in json_list:
        key = el[by]
        new_el = dict()
        try:
            new_el = to_return[key] 
        except KeyError:
            for k in keep:
                new_el[k] = el[k]
                new_el[new] = 0
            to_return[key] = new_el
        new_el[new] += 1
    return to_return


def plot(df):
    print(df)
    data = [ dict(
        type = 'choropleth',
        locations = df['country'],
        z = df['COUNT'],
        text = df['country'],
        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        locationmode = "country names",
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False),
      ) ]

    layout = dict(
        title = 'Banned hosts by denyhosts @ my homeserver',
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection = dict(
                type = 'Mercator'
            ),
            countriescolor="#444444",
            showcountries=True
        )
    )

    fig = dict( data=data, layout=layout )
    py.plot( fig, validate=False, filename='d3-world-map' )

def main():
    file_name = sys.argv[1]
    ips = []
    rgx = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    with open(file_name) as f:
        for line in f:
            ips=ips+rgx.findall(line)
    plot(json_list_todf(map_reduce(get_all_locs(ips),"country_code","COUNT",["country","country_code"])))

if __name__=='__main__':
    main()
