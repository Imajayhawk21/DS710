#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 18:50:18 2024

@author: rajeshgogineni
"""

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
# Import necessary libraries for usage

# For mathematical calculations
import pandas as pd
import numpy as np

# For text cleaning
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# For Plotting
import json

# For webscrapping modules 
import requests 
from bs4 import BeautifulSoup, Comment

#%%
     

def scrape_and_clean_list(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the <dt> tag containing the count
    dt_tags = soup.find_all('dt')
    
    # Extract the text from the <dt> tag
    for dt_tag in dt_tags:
        text = dt_tag.get_text(strip=True)
        print(text)

    return text

#%%

scrape_and_clean_list('https://www.rockclimbing.com/routes')

#%%
# =============================================================================
# Pull Country level description and store in a dataframe as column Description
# =============================================================================

url_country_test = 'https://www.rockclimbing.com/routes/North America/United States/Arizona/Phoenix Area/Bulldog Canyon'

# Send a GET request to the URL
response_country_test = requests.get(url_country_test)

# Check if the request was successful (status code 200)
if response_country_test.status_code == 200:
    # Parse the HTML content of the webpage
    soup_country_test = BeautifulSoup(response_country_test.content, 'html.parser')
    
    print(soup_country_test)
    # Extract the content you're interested in
    # For example, to extract all the text from <p> tags:
    paragraphs = soup_country_test.find_all('p')
    
    # Print the extracted content
    for paragraph in paragraphs:
        print(paragraph.get_text())
else:
    print('Failed to retrieve webpage:', response_country_test.status_code)
    
#%%    detailed_description = None
    
url_country_test = 'https://www.rockclimbing.com/routes/North America/United States/North Dakota/East'

# Send a GET request to the URL
response_country_test = requests.get(url_country_test)  
    
soup = BeautifulSoup(response_country_test.content, 'html.parser')

    
url_last_part = url_country_test.split('/')[-1]

    
# Find the <h3> tag containing "About [Place Name]:"
geography_header_text = soup.find('h3', string=f"About {url_last_part}:")

# If the header is found, find the next <td> tag containing the description
if geography_header_text:
    description_td = geography_header_text.find_next('td', valign='top')
    # Get the description text
    description_text = description_td.get_text(strip=True)

print(description_text)


# # Example usage:
# response_content = response.content  # Assuming 'response' is the response object
# place_name = "Bulldog Canyon"  # Change this to the desired place name
# description = extract_description(response_content, place_name)
# if description:
#     print("Description Text:")
#     print(description)
# else:
#     print(f"No description found for {place_name}")
    
# print(description_text)