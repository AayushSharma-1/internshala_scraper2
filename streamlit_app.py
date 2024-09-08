import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

with open('category1.txt', 'r') as f:
    content = f.read() 
    soup2 = BeautifulSoup(content, 'html.parser')
    CategoryOptions = [tag.text for tag in soup2.find_all('option')]

def get_details(data):
    title = data.find('h3', class_='job-internship-name').text.strip()
    company_name = data.find('div', class_='company_and_premium').find('p').text.strip()
    location = [loc.text for loc in data.find('div', class_='row-1-item locations').find_all('a')]
    # start_date = data.find('span', class_='start_immediately_desktop').text if data.find('span', class_='start_immediately_desktop') else "Not Available"
    duration = re.findall(r'<i class="ic-16-calendar"></i>\s*<span>([^<]+)</span>', str(dee[0].find_all('div', class_='row-1-item')))[0].strip()
    stipend = re.findall('₹ \d+.\d+.[^/]+',str(dee[0].find('span', attrs = {'class' : 'stipend'})))[0].strip()
    # status = data.find_all('i', class_='ic-16-reschedule')[0].next_sibling.strip()
    # links = 'https://internshala.com' + data.find('a', class_='btn btn-secondary view_detail_button_outline')['href']
    
    return {
        "Title": title,
        "Company Name": company_name,
        "Location": location,
        # "Start Date": start_date,
        "Duration": duration,
        "Stipend": stipend,
        # "Status": status,
        # "Links": links
    }

st.write(""" # Internshala Scraper""")
selections = st.sidebar.multiselect('Pick The Domains', CategoryOptions)
link = 'https://internshala.com/internships/'
for i in range(len(selections)):    
    selections[i] = ','+selections[i].replace(" ", '-').lower()
    link+=selections[i]

print(link)

response = requests.get(link + '-internship/')
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    total_pages = int(soup.find('span', id="total_pages").text)
    num_of_pages = st.sidebar.slider('Number of Internshala pages to Scrape', max_value=total_pages)
    
    dict_of_data = []
    for j in range(1, num_of_pages+1):
        res_link = f"{link + '-internship'}/page-{j}"
        print(res_link)
        res = requests.get(res_link)
        print(res.status_code)
        res_soup = BeautifulSoup(res.content, 'html.parser')
        dee = res_soup.find_all('div', attrs={'class' :'container-fluid individual_internship view_detail_button visibilityTrackerItem'})
        # print(dee)
        for item in dee:
            dict_of_data.append(get_details(item))

    df = pd.DataFrame(dict_of_data)
    df.index = pd.RangeIndex(start = 1, stop = len(df) + 1, name = 'Index')
    st.dataframe(df, use_container_width=True)
else: 
    print("Status code not 200")