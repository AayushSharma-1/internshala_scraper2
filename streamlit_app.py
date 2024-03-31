import pandas as pd
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
# import category

# file_path = input('Enter the File path')

with open('category1.txt', 'r') as f:
    content = f.read() 
    soup2 = BeautifulSoup(content, 'html.parser')
    CategoryOptions =[]
    for tag in soup2.find_all('option', attrs = {}):
        CategoryOptions.append(tag.text)
    f.close()    

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
selections = st.sidebar.multiselect(
        'Pick The Domains',
        CategoryOptions
    )
link = 'https://internshala.com/internships/'

for i in range(len(selections)):    
    selections[i] = ','+ selections[i].replace(" ", '-').lower()
    link+=selections[i]

print(link + '-internship/')    

response = requests.get(link + '-internship/')
print('Response = ' + str(response.status_code))
    
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    print("Parsed Landing Page")
    
    link_soup = soup.find('span', attrs = {'id':"total_pages"}).text
    total_pages = int(link_soup)
    num_of_pages = st.sidebar.slider('Number of Internshala pages to Scrape',max_value=total_pages )
    

dict_of_data = []
for j in range(1,num_of_pages+1):
    
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
# lat = []
# lon = []
# for i in df['locations']:
    
#     df2 = pd.DataFrame({
#         'lat' :  [18.521428, 28.5706333],
#         'lon' : [73.8544541,77.3272147]
#     })
# value = st.sidebar.toggle('Do You want location on Maps ?')
# if(value):
#     st.map(df2, size = 50)
