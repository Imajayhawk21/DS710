#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 19:57:53 2024

@author: rajeshgogineni
"""

#%%

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
# Import necessary libraries for usage

# For mathematical calculations
import pandas as pd

# For Plotting
import matplotlib.pyplot as plt
import seaborn as sns

import cartopy.crs as ccrs
import cartopy.feature as cfeature

# For webscrapping modules 
import requests 
from bs4 import BeautifulSoup

#%%
# =============================================================================
# Task 1.1
# =============================================================================

# Create object from the selected url
url_lakes = 'https://en.wikipedia.org/wiki/List_of_lakes_of_Western_Australia,_A%E2%80%93C'
response_lakes = requests.get(url_lakes)

#%%

# Pull html text from html content
html_content_lakes = response_lakes.text

# Parse the HTML content using BeautifulSoup
soup_lakes = BeautifulSoup(html_content_lakes, 'html.parser')

#%% 
# =============================================================================
# Task 1.2
# =============================================================================

# Find all table elements in the HTML content
tables_lakes = soup_lakes.find_all('table')

#%%

# Iterate over each table and extract the data into a list of lists
table_data = []
for table in tables_lakes:
    # Extract the data from each row (tr = table row) 
    rows = table.find_all('tr')
    table_rows = []
    for row in rows:
        # Extract the data from each cell in the row
        # td = table data, th = table header
        cells = row.find_all(['td', 'th'])
        row_data = []
        for cell in cells:
            row_data.append(cell.get_text(strip=True))
        table_rows.append(row_data)
    table_data.append(table_rows)

# Convert the list of lists into a list of DataFrames
dfs = []
for data in table_data:
    df = pd.DataFrame(data[1:], columns=data[0]) 
    dfs.append(df)

print(dfs)

# Concatenate all DataFrames into a single DataFrame
lakes_df = pd.concat(dfs, ignore_index=True)

print(lakes_df)

#%%

# Clean up dataframe if Remarks is still in it 
if 'Remarks' in lakes_df.columns:
    lakes_df = lakes_df.drop(columns=['Remarks'])


#%%
# =============================================================================
# Task 1.3
# =============================================================================

# Split the contents of the column by '/'
if 'Coordinates' in lakes_df.columns:
    split_values = lakes_df['Coordinates'].str.split('/').str[-1]

# Assign the split values to new columns
lakes_df['Lat_Long_Rough_Coordinates'] = split_values

# Split column into Latitude and Longitude Columns
if 'Latitude' not in lakes_df.columns: 
    lakes_df['Latitude'] = (lakes_df['Lat_Long_Rough_Coordinates'].str.split(';').str[0]) 
if 'Longitude' not in lakes_df.columns: 
    lakes_df['Longitude'] = lakes_df['Lat_Long_Rough_Coordinates'].str.split(';').str[1]

# Clean Latitude and Longitude Columns 
if 'Latitude' in lakes_df.columns: 
    lakes_df['Latitude'] = lakes_df['Latitude'].apply(lambda x: ''.join(filter(lambda c: c.isdigit() or c == '.' or c == '-', x.replace(' ', ''))))
if 'Longitude' in lakes_df.columns: 
    lakes_df['Longitude'] = lakes_df['Longitude'].apply(lambda x: ''.join(filter(lambda c: c.isdigit() or c == '.', x.replace(' ', ' '))))

# Convert columns from strings to floats
if lakes_df['Latitude'].dtype == 'object':
     lakes_df['Latitude'] = lakes_df['Latitude'].astype(float)
if lakes_df['Longitude'].dtype == 'object':
     lakes_df['Longitude'] = lakes_df['Longitude'].astype(float)


#%%
# =============================================================================
# Task 1.4
# =============================================================================

def lakes_lat_long_australia(df):
    
    # Define the boundaries of Western Australia
    # [minlon, maxlon, minlat, maxlat]
    boundaries = [110, 130, -35, -15]  
    
    # Create a map with Cartopy
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    # Set the extent of the map to Western Australia
    ax.set_extent(boundaries)
    
    # Add coastline and borders
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.BORDERS)
    
    # Add title
    ax.set_title('Map of Western Australia')
    
    # Overlay data (e.g., points)
    ax.scatter(df['Longitude'], df['Latitude'], color='blue', marker='x', s=50)

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_plot_assign7_task1-4.png')
            
    return    
#%%
# Run function and verify it works

lakes_lat_long_australia(lakes_df)

#%%
# =============================================================================
# Task 2.1
# =============================================================================

# Create object from the selected url
url_building = 'https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_the_United_States'
response_buildings = requests.get(url_building)

#%%

# Pull html text from html content
html_content_buildings = response_buildings.text

# Parse the HTML content using BeautifulSoup
soup_buildings = BeautifulSoup(html_content_buildings, 'html.parser')

#%%
# =============================================================================
# Task 2.2
# =============================================================================

# Find all table elements in the HTML content
tables_buildings = soup_buildings.find_all('table')

# Convert table to DataFrame
if tables_buildings:
    buildings_df = pd.read_html(str(tables_buildings))[0]
    
# Use DataFrame.loc to keep only relevant columns for our dataframe
columns_to_keep = ['Name', 'Height ft (m)', 'Floors', 'Year']
buildings_df = buildings_df.loc[:, columns_to_keep]

#%%
# =============================================================================
# Task 2.3
# =============================================================================

# We need to split the Height ft (m) column where there is a space in the column
if 'Height' not in buildings_df.columns: 
    buildings_df['Height'] = buildings_df['Height ft (m)'].str.split(' ').str[0]
    buildings_df['Throwaway Column'] = buildings_df['Height ft (m)'].str.split(' ').str[1]

# Clean up column using a lambda function. We want to keep the digits and get rid of the rest
buildings_df['Height'] = buildings_df['Height'].apply(lambda x: ''.join(filter(lambda c: c.isdigit() or c == '.', x.replace(',', ''))))

# Convert columns from strings to integer
if buildings_df['Height'].dtype == 'object':
    buildings_df['Height'] = buildings_df['Height'].astype(int)

#%%
# =============================================================================
# Task 2.4
# =============================================================================

# Slice dataframe and get back everthing that is a 1000 ft or greater
desired_building_height = 1000
filter_value = buildings_df['Height'] >= desired_building_height
buildings_1000_df = buildings_df[filter_value]

#%%
# =============================================================================
# Task 2.5
# =============================================================================

def height_tallest_buildings(df):
    
    # Created a Figure object
    fig = plt.figure(figsize=(10, 8))
        
    # Use Seaborn library to put markers on bar graph
    sns.barplot(data=df, x='Name', y='Height')

    # Added labels and title
    plt.xlabel('Name of Building')
    plt.ylabel('Height (ft)')
    plt.title('Worlds Tallest Buildings')
    plt.xticks(rotation=90)

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_assign7_task2-5.png')
            
    return  

#%%

height_tallest_buildings(buildings_1000_df)

