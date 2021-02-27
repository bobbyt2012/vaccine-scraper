from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import pandas as pd

df = pd.DataFrame(columns = ['Facility','Address','Phone','ApptDatetime','VaccineType','URL'])

def mt_carmel(link, vaccine):
    
    inner_df = pd.DataFrame()
    
    page_link = link
    page_response = requests.get(page_link, timeout = 15)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    #Location, Facility, Phone URL
    facility = page_content.find('li', {'class', 'facility'}).get_text().strip()
    address = page_content.find('li', {'class', 'location'}).get_text().replace('•','')
    address = ' '.join(address.split())
    phone = page_content.find('li', {'class', 'phone'}).get_text()

    a_tags = page_content.find_all('a', {'class', 'button secondary'})

    for x in a_tags:  
        num_dt = x['href']
        num_dt = num_dt.split('at=', 1)[1]
        date_obj = datetime(year=int(num_dt[0:4]), month=int(num_dt[4:6]), day=int(num_dt[6:8]), hour=int(num_dt[8:10]), minute=int(num_dt[10:12]))

        date = datetime.strftime(date_obj,'%Y-%m-%d %I:%M %p')

        data = [{'Facility': facility, 'Address': address, 'Phone':phone,
                 'ApptDatetime':date,
                 'VaccineType': vaccine,
                 'URL': page_link}]
        
        inner_df = inner_df.append(data, ignore_index = True, sort = False)
    

    return inner_df

data = mt_carmel(link = 'https://mountcarmelhealth.inquicker.com/employee-vaccination-covid-19-scheduling/discharge/provider/mcmg-moderna-covid-vaccine-dose-1', vaccine = 'Moderna')
df = df.append(data, ignore_index = True, sort = False)

data = mt_carmel(link = 'https://mountcarmelhealth.inquicker.com/employee-vaccination-covid-19-scheduling/discharge/provider/mcmg-pfizer-covid-vaccine-dose-1', vaccine = 'Pfizer')
df = df.append(data, ignore_index = True, sort = False)
