import requests
from bs4 import BeautifulSoup
import pandas as pd
file_path = input('Enter the File path')

with open(file_path, 'r') as f:
    content = f.read() 
    soup2 = BeautifulSoup(content, 'html.parser')
    CategoryOptions =[]
    for tag in soup2.find_all('option', attrs = {}):
        CategoryOptions.append(tag.text)
    f.close()       