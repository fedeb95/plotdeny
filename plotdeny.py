import requests
import sys
import re
import time
import pandas as pd

def get_location(ip):
    return requests.get("http://ip-api.com/json/"+ip).json()

def get_all_locs(ip_list):
    count = 0
    data = []
    for ip in ip_list:
        count += 1
        if count > 140:
            count = 0
            time.sleep(90)
        data.append(get_location(ip))
    return data

def json_list_todf(json_list):
    return pd.DataFrame(json_list) 

def main():
    file_name = sys.argv[1]
    ips = []
    rgx = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    with open(file_name) as f:
        for line in f:
            ips=ips+rgx.findall(line)
    print(json_list_todf(get_all_locs(ips)))

if __name__=='__main__':
    main()
