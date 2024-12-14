#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:09:49 2024

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
import matplotlib.pyplot as plt
import seaborn as sns
import json

# For webscrapping modules 
import requests 
from bs4 import BeautifulSoup

#%%

url = 'https://www.rockclimbing.com/routes/North_America/Canada'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(soup)
    # Extract the content you're interested in
    # For example, to extract all the text from <p> tags:
    paragraphs = soup.find_all('p')
    
    # Print the extracted content
    for paragraph in paragraphs:
        print(paragraph.get_text())
else:
    print('Failed to retrieve webpage:', response.status_code)