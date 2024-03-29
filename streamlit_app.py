import pandas as pd
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def get_details(data):
    title = ''
    company_name = '' 
    location = []
    start_date = ''
    duration = ''
    stipend =''
    status = ''
    links = ''
    pattern_for_status = '<i class=\"ic-16-reschedule\"></i>([^<]+)'
    # data = BeautifulSoup(data,'html.parser')
    title = data.find('h3', attrs = {'class' : 'heading_4_5 profile'}).text.strip()
    company_name = re.findall('<p>\s(.*?)</p>', str(data.find('div', attrs = {'class': 'company_and_premium'})))[0].strip()
    location.append(re.findall('>(.*?)</a>',str(data.find('div', attrs = {'id': 'location_names'})) ))
    try:
        start_date = data.find('span', attrs={'class': 'start_immediately_desktop'}).text
    except AttributeError:
        try:
            start_date = data.find('div', attrs={'id': 'start-date-first'}).text
        except AttributeError:
            start_date = "Not Available"

        
    duration = data.find('div', attrs = {'class' : 'item_body'}).text.strip()
    stipend = data.find('span', attrs = {'class' : 'stipend'}).text.strip()
    status = re.findall(pattern_for_status , str(dee[0]))[0]
    links = data.find('a', attrs = {'class' : 'btn btn-secondary view_detail_button_outline', 'href' : True}).get('href')
    
    data = {
    "Title": title,
    "Company Name": company_name,
    "Location": location,
    "Start Date": start_date,
    "Duration": duration,
    "Stipend": stipend,
    "Status": status,
    "Links": 'https://internshala.com' + links
    }
    
    return data
        
st.write(""" # Internshala Scraper""")



link = 'https://internshala.com/internships/big-data,data-analysis,data-analytics,data-science,machine-learning,python-internship/'

response = requests.get(link)
print('Response = ' + str(response.status_code))
    
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    print("Parsed Landing Page")
    
    link_soup = soup.find('span', attrs = {'id':"total_pages"}).text
    total_pages = int(link_soup)
    num_of_pages = st.sidebar.slider('Number of Internships to Scrape',min_value=1 ,max_value=total_pages )

dict_of_data = []
for j in range(1,num_of_pages):
    
    res_link = link + 'page-' + str(j)
    res = requests.get(res_link)
    res_soup = BeautifulSoup(res.content, 'html.parser')
    dee = res_soup.find_all('div', attrs = {'class' : 'container-fluid individual_internship visibilityTrackerItem'})
    
    for i in range(len(dee)):
        dict_of_data.append(get_details(dee[i]))

dict_of_data2 = {}
for i in range(len(dict_of_data)):
    dict_of_data2[i] = dict_of_data[i]

df = pd.DataFrame.from_dict(dict_of_data2, orient='index')

st.dataframe(df)