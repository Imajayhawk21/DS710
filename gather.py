#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:09:49 2024

@author: rajeshgogineni
"""

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%% Required Libraries

# For mathematical calculations
import pandas as pd
import numpy as np

# Set display options to show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 30)

# For text cleaning
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# For Plotting
#import json

# For webscrapping modules 
import requests 
from bs4 import BeautifulSoup#, Comment
import time
from urllib.parse import quote_plus

# Performance checking
import concurrent.futures
from retrying import retry

#%% Initial Configuration for Exceptions, Wait Time and Language Removal

# Initialize dictionary to store exceptions
exception_dict = {'Exception': [], 'Count': []}

# Rules behind retry logic 
retry_config = {
    'wait_exponential_max': 20000,        # Maximum wait time between retries
    'wait_exponential_multiplier': 10000,  # Initial wait time between retries
    'stop_max_delay': 4000000,           # Maximum total time for retries (milliseconds) 
    'stop_max_attempt_number': 3,     # Maximum number of retry attempts
    'retry_on_exception': lambda exc: isinstance(exc, Exception),  # Retry on any exception
    'wait_jitter_max': 7000,              # Maximum jitter to introduce into wait time
}

# stopwords for different languages so we can remove these from analysis later
stopwords_english = nltk.corpus.stopwords.words('english')
stopwords_spanish = nltk.corpus.stopwords.words('spanish')
stopwords_french = nltk.corpus.stopwords.words('french')
stopwords_german = nltk.corpus.stopwords.words('german')

# Initialize the SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

#%% Calculation of time and pass or failure

def retry_communication(url, url_last_part):
    
    start_time = time.time()
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Request failed after {time_taken} seconds: {e}")
        # Process response data here
        exception_dict['Exception'].append(str(e))
        exception_dict['Count'].append(1)
        # Log or handle the failure here
        raise  # Re-raise the exception to trigger retries
    else:
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Request completed successfully for {url_last_part} in {time_taken} seconds.")
    
    return exception_dict, response

#%% Function used for scraping entity names and route counts

@retry(**retry_config)
def scrape_and_clean_list(url):
    
    url_last_part = url.split('/')[-1]  # Extract the last part of the URL
    
    print(f"Running Scrape and Clean Function for {url_last_part}")
    
    exception_dict, response = retry_communication(url, url_last_part)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize lists for later appending
    entity_name=[]
    route_count=[]
    
    # Find the <dt> tag containing the count
    dt_tags = soup.find_all('dt')
    
    # Extract the text from the <dt> tag
    for dt_tag in dt_tags:
        text = dt_tag.get_text(strip=True)
        
        name, count_with_parenthesis = text.split("(")
        count = int(count_with_parenthesis.strip(")"))
        
        # Append to lists 
        entity_name.append(name) 
        route_count.append(count)
    
    return entity_name, route_count

#%% Dictionary Creation for Countries, States and Regions

@retry(**retry_config)
def dict_creation(url, country_split, continent_split, state=None):
    
    # Initialize an empty dictionary to store states/regions by country
    states_regions_dict = {}
        
    url_last_part = url.split('/')[-1]  # Extract the last part of the URL

    print(f"Dictionary Creation Function for {url_last_part}")

    exception_dict, response = retry_communication(url, url_last_part)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the <h3> tag containing "States:" or "Regions:"
    states_header = soup.find('h3', class_='noseparator', string=lambda text: 'States:' in text or 'Regions:' in text)
    
    if states_header:
        # Get the text content of the <h3> tag
        header_text = states_header.get_text(strip=True)
    
        # Extract the country name and continent from the URL
        url_country = url.split('/')[country_split]  
        url_continent = url.split('/')[continent_split] 

        # Determine if the country contains only regions or both states and regions
        if 'Regions:' in header_text:
            # Country contains only regions
            regions_only = True
        else:
            # Country contains both states and regions
            regions_only = False
    
        # Find the <div> containing the list of states or regions
        catlisting_div = states_header.find_next('div', id='catlisting')
    
        # Initialize an empty list to store states or regions
        states_regions_list = []
    
        # Find all <dl> elements within the <div>
        dl_elements = catlisting_div.find_all('dl')
    
        # Iterate over <dl> elements to extract states or regions
        for dl_element in dl_elements:
            # Find all <dt> elements within the <dl>
            dt_elements = dl_element.find_all('dt')
    
            # Extract the text content of each <dt> element
            states_regions_list.extend([dt.get_text(strip=True) for dt in dt_elements])
    
        # Store the states or regions list along with the country name and flag in the dictionary
        if state is not None:
            states_regions_dict = {'Continent_Name': url_continent, 'Country_Name': url_country, 'State': state, 'regions_only': regions_only, 'list': states_regions_list}
        
        else:
            states_regions_dict = {'Continent_Name': url_continent, 'Country_Name': url_country, 'regions_only': regions_only, 'list': states_regions_list}   

        return states_regions_dict

#%% Removing Stop Words From Description Columns for Sensitivity Analysis

def remove_stopwords(text):
    
    # List of languages for stop words removal
    #languages = ['english', 'german', 'spanish', 'french', 'italian']
    if text is None:
        return text
    
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Remove stopwords from the words
    filtered_words = [word for word in words if word.lower() not in stopwords_english]
    
    # Join the remaining words back into a string
    processed_text = ' '.join(filtered_words)
    
    return processed_text


#%% Sentiment Analysis

def perform_sentiment_analysis(df, description_column):
    # Filter out rows where the description is not empty
    valid_rows = df[description_column].notna()
    valid_rows_df = df[valid_rows]

    # Apply sentiment analysis to valid rows
    sentiment_scores_list = []
    for description in valid_rows_df[description_column]:
        sentiment_scores_list.append(sid.polarity_scores(description))

    # Create DataFrame from sentiment scores
    sentiment_scores_df = pd.DataFrame(sentiment_scores_list, columns=['neg', 'neu', 'pos', 'compound'])

    # Concatenate sentiment_scores_df to main_df
    main_df = pd.concat([valid_rows_df.reset_index(drop=True), sentiment_scores_df.reset_index(drop=True)], axis=1)

    return main_df

#%% Extract detailed information from the very detailed webpages

# =============================================================================
# Change this from "Regions:", "Climbing Areas:", or "Climbing Sections:"
# =============================================================================

@retry(**retry_config)
def extract_desired_section(url, area_in_html, index):
    
    geography_with_counts = []
    description_text = None
    
    # Extract the last part of the URL
    url_last_part = url.split('/')[-1]  

    print(f"Extract Desired Section Function for {url_last_part}")

    exception_dict, response = retry_communication(url, url_last_part)
        
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the <h3> tag with text "Regions:"
    geography_header = soup.find('h3', string=area_in_html)

    # If the header is found
    if geography_header:
        # Find the next <div> tag with id "catlisting" after the header
        cat_listing_div = geography_header.find_next_sibling('div', id="catlisting")

        # If the div is found
        if cat_listing_div:
            # Find all <dt> tags within the div
            dt_tags = cat_listing_div.find_all('dt')

            # Extract the text from the <a> tags and their adjacent <dt> tags
            for dt_tag in dt_tags:
                a_tag = dt_tag.find('a')
                if a_tag:
                    geography = a_tag.get_text(strip=True)
                    count_text = dt_tag.get_text(strip=True)
                    count = count_text.split('(')[-1].split(')')[0]
                    geography_with_counts.append((geography, count))
    
    # Find the <h3> tag containing "About [Place Name]:"
    geography_header = soup.find('h3', string=f"About {url_last_part}:")
    
    # If the header is found, find the next <td> tag containing the description
    if geography_header:
        description_td = geography_header.find_next('td', valign='top')
        # Get the description text
        description_text = description_td.get_text(strip=True)
        
    # Function to remove stopwords
    if description_text:
        processed_description = remove_stopwords(description_text)
        
    else:
        processed_description = None
    
    # Return all relevant data
    return geography_with_counts, index, processed_description

#%% Function to handle URL encoding

def encode_url(url):
    
    url = url.replace('š', '__353_') 
    url = url.replace('č', '__269_') 
    url = url.replace('ž', '__382_') 
    url = url.replace('ş', '__351_') 
    url = url.replace('Č', '__268_') 
    url = url.replace('İ', '__304_') 
    url = url.replace('ğ', '__287_') 
    
    special_characters = 'äüößÁáÄäÖöÜüßÁáÉÍíÓóÚúÀàÈèéÌìÒòÙùÂâÊêÎîÔôÛûÇçÑñø+&ª´åČã?'
    for char in special_characters:
        url = url.replace(char, '_')
    
    # Encode the URL using quote_plus
    encoded_url = quote_plus(url, safe='/:@.-~=?äüößÁáÄäÖöÜüßÁáÉÍíÓóÚúÀàÈèÌìÒòÙùÂâÊêÎîÔôÛûÇçÑñøı')

    return encoded_url

#%% Process Function for State Multi Thread Execution

def process_url_state(url, state):
    
    return dict_creation(url, -2, -3, state)

#%% Detail Climbing Information on Routes Page
 
# =============================================================================
# To pull route detail information out of last webpage
# =============================================================================

@retry(**retry_config)
def extract_climbing_route_details(url, index):
    
    # Initialize variables to store extracted details
    rating = None
    difficulty_rating = None
    climbing_type = None
    rock_type = None
    ascents_count = None
    climbing_routes_list = [] 
    
    # Extract the last part of the URL
    url_last_part = url.split('/')[-1] 
    
    print(f"Extracting Route Details for {url_last_part}")
    
    exception_dict, response = retry_communication(url, url_last_part)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the element containing climbing type information
    climbing_type_element = soup.find('td', class_='noborder', string='Type of Climbing:')
    if climbing_type_element:
        climbing_type = climbing_type_element.find_next_sibling('td').get_text(strip=True)
        
    rock_type_element = soup.find('td', class_='noborder', string='Rock Type:')
    if rock_type_element:
        rock_type = rock_type_element.find_next_sibling('td').get_text(strip=True)
        
    # Extract rating
    rating_element = soup.find('img', alt=lambda x: x and 'Average Rating' in x)
    if rating_element:
        rating_text = rating_element.get('title')
        if rating_text:
            rating_start_index = rating_text.find('=') + 2
            rating_end_index = rating_text.find('/5')
            rating = rating_text[rating_start_index:rating_end_index]
    
    # Find all <td> tags with class 'ftablecol'
    td_elements = soup.find_all('td', class_='ftablecol')
    
    # Extract the ascents count and difficulty rating
    ascents_count = td_elements[0].text.strip()
    difficulty_rating = td_elements[3].text.strip()
    
    climbing_routes_list.append((rock_type, climbing_type, rating, difficulty_rating, ascents_count))

    return climbing_routes_list, index

#%% Process data for creation, naming and filtering of columns

def column_split(df, main_column, new_column_name):
    
    # Split the 'list' column into multiple columns based on the parentheses
    new_df = df[main_column].str.split('(', expand=True)
    
    # Extract the region and count into separate columns
    if new_column_name not in new_df:
        df[new_column_name] = new_df[0]
        df[f"{new_column_name}_Route_Count"] = new_df[1].str.rstrip(')')

    # Handle invalid literals by excluding rows with invalid literals
    try:
        df[f"{new_column_name}_Route_Count"] = pd.to_numeric(df[f"{new_column_name}_Route_Count"], errors='coerce')
        df = df[df[f"{new_column_name}_Route_Count"].notna()]
    except ValueError as e:
         print("An error occurred:", e)
    
    if new_column_name in df:
        df[f"{new_column_name}_Route_Count"] = df[f"{new_column_name}_Route_Count"].astype(int)
    
    # Drop the original 'list' column
    if main_column in df: 
        df.drop(columns=[main_column], inplace=True)
        
    df = df.drop_duplicates()

    df = df[df[f"{new_column_name}_Route_Count"] > 0]
      
    return df

#%% Function used for exploding a dataframe and then being able to merge back

# =============================================================================
# Explode lists due to many observations then bring things back together
# =============================================================================

def explode_and_merge(df, key_column, merge_columns=None):
    
    # Check if merge_columns is provided and is a list
    if merge_columns is not None and not isinstance(merge_columns, list):
        raise ValueError("merge_columns must be a list")
    
    # If merge_columns is not provided, initialize it as an empty list
    if merge_columns is None:
        merge_columns = []
    
    # Explode out list to individual observations
    df = df.explode(key_column)
    
    # Merge the exploded dataframe back with the original dataframe
    df = pd.merge(df[merge_columns], 
                                  df.drop(columns=merge_columns), 
                                  left_index=True, 
                                  right_index=True)
    
    return df


#%% Exception Reporting 

def error_tracking(exception_list, df):
    
    # After processing all URLs, print exceptions and aggregate them into a DataFrame
    if exception_list:
        print("Exceptions occurred:")
        for exception in exception_list:
            print(exception)
    
        # Count occurrences of each exception
        exception_counts = {str(exception): exception_list.count(exception) for exception in set(exception_list)}
        
        # Create a DataFrame from the exception counts
        exceptions_df = pd.DataFrame(list(exception_counts.items()), columns=['Exception', 'Count'])
        print("\nExceptions DataFrame:")
        print(exceptions_df.shape)
        print(exceptions_df)
        return exceptions_df
    else:
        print("No exceptions occurred.")
        
        return None


#%% Main Function that creates all corresponding dataframes for analysis

# =============================================================================
# To create dataframes from our results
# =============================================================================

BASE_URL = 'https://www.rockclimbing.com/routes'

def select_a_region(url):
    # Createda global variable due to overwriting on two with statements towards the end
    global BASE_URL
    
    # To Create continent Dataframe    
    try:
        entity_name, route_count = scrape_and_clean_list(url)
    except Exception as e:
        print(f"All retry attempts failed. Returning empty dictionary.")
        entity_name, route_count = {}, {}
    
    continent_route_df = pd.DataFrame({'Continent_Name': entity_name, 'Route Count': route_count})
        
     # Initialize lists for later utilization
    country_entity_name=[]
    country_route_count=[]
    all_continents=[]
    url_list=[]
    
    # Create list of URLs
    for continent in continent_route_df['Continent_Name']:
        country_url_parts = [url, continent] 
        country_url = '/'.join(country_url_parts)
        url_list.append(country_url)
        
    # Execute the function in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        results = executor.map(scrape_and_clean_list, url_list)
    
    # Process the results
    for continent, result in zip(continent_route_df['Continent_Name'], results):
        country_entity_name.extend(result[0])
        country_route_count.extend(result[1])
        all_continents.extend([continent] * len(result[0]))

    # Create the DataFrame
    country_route_df = pd.DataFrame({'Continent_Name': all_continents, 'Country_Name': country_entity_name, 'Country_Route_Count': country_route_count})
        
# =============================================================================
# States and Regions Extraction and Column Creation First Pass
# =============================================================================
    
    dfs_round_one_regions = []    
    url_list=[]
    exception_list = []

    # Create the URL column by combining other columns
    country_route_df['Continent_Country_Url'] = url + '/' + country_route_df['Continent_Name'] + '/' + country_route_df['Country_Name'] 
    
    country_route_df = country_route_df.set_index(['Continent_Name', 'Country_Name'], drop=False)
    
    # Reduce size of problem by filtering dataframes as we go
    country_route_df = country_route_df[country_route_df['Country_Route_Count'] > 0]
    
    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        # Submit tasks for each URL
        futures = [
            executor.submit(
                lambda url: dict_creation(url, -1, -2),
                url
            )
            for url in country_route_df['Continent_Country_Url']
        ]
        
        # Wait for all tasks to complete
        done, _ = concurrent.futures.wait(futures)
        
        # Iterate over completed tasks
        for future in done:
            try:
                # Get the result of the task
                regions_dict = future.result()
                
                # Append the dictionary to the list
                dfs_round_one_regions.append(regions_dict)
            except Exception as e:
                exception_list.append(e)
                print(f"Error processing URL: {e}")  
    
    executor.shutdown(wait=True)
        
# =============================================================================
# Cleaning up columns, exploding and merging a dataframe
# =============================================================================

    # Convert the list of dictionaries to a DataFrame
    states_regions_round_one_df = pd.DataFrame(dfs_round_one_regions).dropna(how='all')
    
    # Print exceptions with the dataframe
    error_tracking(exception_list, states_regions_round_one_df)

    # Only return regions_only = True
    regions_only_filtered_df = states_regions_round_one_df[states_regions_round_one_df['regions_only']== True]
    
    # Function to explode and merge using list
    regions_only_merged_df = explode_and_merge(regions_only_filtered_df, 'list', merge_columns=['Continent_Name', 'Country_Name', 'regions_only'])
    
    # Set index of dataframe
    regions_only_merged_df = regions_only_merged_df.set_index(['Continent_Name', 'Country_Name', 'list', 'regions_only'], drop=False)
        
    # Split the 'list' column into multiple columns based on the parentheses
    regions_only_merged_df = column_split(regions_only_merged_df, 'list', 'Region')

# =============================================================================
# Create base dataframe for usage for our states only for loop later
# =============================================================================
    
    states_only_filtered_df = states_regions_round_one_df[states_regions_round_one_df['regions_only']== False]
        
    # Function to explode and merge using list
    merged_df = explode_and_merge(states_only_filtered_df, 'list', merge_columns=['Continent_Name', 'Country_Name', 'regions_only'])
       
    # # Set index of dataframe
    merged_df = merged_df.set_index(['Continent_Name', 'Country_Name', 'list', 'regions_only'], drop=False)
    
    # Splitting columns and formatting those two new columns
    merged_df = column_split(merged_df, 'list', 'State')
                
    # Remove any states that have a value of zero routes
    merged_df = merged_df[merged_df['State_Route_Count'] > 0]
    
# =============================================================================
# Rerun states through a for loop and functions to get regions for these   
# =============================================================================

    dfs_round_two_states_regions = []
    exception_list = []
    
    # Create the URL column by combining other columns
    merged_df['Country_States_Url'] = url + '/' + merged_df['Continent_Name'] + '/' + merged_df['Country_Name'] + '/' + merged_df['State']
    
    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        
        # Submit tasks for each URL
        futures = [executor.submit(process_url_state, url, state) for url, state in zip(merged_df['Country_States_Url'], merged_df['State'])]
    
        # Wait for all tasks to complete
        done, _ = concurrent.futures.wait(futures)
        
        # Iterate over completed tasks
        for future in done:
            try:
                # Get the result of the task
                states_to_get_regions_dict = future.result()
                
                # Append the dictionary to the list
                dfs_round_two_states_regions.append(states_to_get_regions_dict)
            except Exception as e:
                exception_list.append(e)
                print(f"Error processing URL: {e}")
        
    # Shut down the executor
    executor.shutdown(wait=True)
    
    # Convert the list of dictionaries to a DataFrame
    dfs_round_two_states_regions_df = pd.DataFrame(dfs_round_two_states_regions)
    
    # Print exceptions with the dataframe
    error_tracking(exception_list, dfs_round_two_states_regions_df)
    
    dfs_round_two_states_regions_df = dfs_round_two_states_regions_df.dropna(how='all')

# =============================================================================
# We have to break out the dfs_round_two_states_regions like before so we get 
# region and region route counts
# =============================================================================
    
    states_with_regions_merged_df = explode_and_merge(dfs_round_two_states_regions_df, 'list', merge_columns=['Continent_Name', 'Country_Name', 'regions_only'])
    
    # Extract the region and count into separate columns
    states_with_regions_df = column_split(states_with_regions_merged_df, 'list', 'Region')
    
# =============================================================================
# Merge two state dataframes together
# =============================================================================

    states_combined_df = pd.merge(merged_df,states_with_regions_df, on=['State'], how='right')
    
# =============================================================================
# Grab region dataframe and add State and State_Route_Count columns with NaN values
# =============================================================================
    
    regions_only_merged_df['State'] = np.nan
    regions_only_merged_df['State_Route_Count'] = np.nan
    
# =============================================================================
# Drop columns, rename columns
# =============================================================================
    
    states_combined_df = states_combined_df.drop(columns=['regions_only_x', 'regions_only_y', 'Country_States_Url', 'Continent_Name_y',
    'Country_Name_y'])
    
    # Rename columns to make them more understandable
    states_combined_df = states_combined_df.rename(columns={ 'Continent_Name_x': 'Continent_Name', 'Country_Name_x': 'Country_Name'})

    regions_only_merged_df = regions_only_merged_df.reset_index(drop=True)

    regions_only_merged_df = regions_only_merged_df.drop(columns=['regions_only'])
    
# =============================================================================
# Concat state and region dataframes
# =============================================================================
         
    # Stack the DataFrames vertically and sort by multiple columns
    stacked_df = pd.concat([states_combined_df, regions_only_merged_df], axis=0)
    
    stacked_df.reset_index(drop=True, inplace=True)    

# =============================================================================
# CLIMBING AREA LOOP
# =============================================================================
    
    # Initialize Lists/Dictionarieis
    dfs_climbingareas = []
    exception_list = []
    future_to_url = {}
    
# =============================================================================
# Create data column to loop over
# =============================================================================

    # Create the URL column to iterate over
    stacked_df['URL'] = url + '/' + stacked_df['Continent_Name'] + '/' + stacked_df['Country_Name']
    # Add State and Region if State is not NaN
    stacked_df.loc[stacked_df['State'].notna(), 'URL'] += '/' + stacked_df['State']
    stacked_df['URL'] += '/' + stacked_df['Region']
    # Apply URL encoding, excluding NaN values
    stacked_df['URL'] = stacked_df['URL'].apply(lambda x: encode_url(x) if pd.notna(x) else x)
    
    stacked_df.drop_duplicates()
    
    # Process URLs using concurrent futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        # Iterate over each row in the DataFrame
        for index, row in stacked_df.iterrows():
            try:
                if not row['Region_Route_Count']:  
                    print(f"Skipping record with index {index} as it has no climbing routes.")
                    continue  
                # Construct the URL for the current row
                url = row['URL']
                # Submit task for the current URL
                future = executor.submit(extract_desired_section, row['URL'], "Climbing Areas:", index)
                # Store the future in the dictionary
                future_to_url[future] = index
            except Exception as e:
                print(f"Error processing row {index}: {e}")
    
        # Iterate over completed tasks
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                climbing_areas_list, index, processed_description = future.result()            
                if climbing_areas_list is not None:
                    # Create a DataFrame for climbing areas data
                    climbing_areas_df = pd.DataFrame(climbing_areas_list, columns=['Climbing_Area', 'Climbing_Area_Route_Count'])
                    climbing_areas_df['Continent_Name'] = stacked_df.loc[index, 'Continent_Name']
                    climbing_areas_df['Country_Name'] = stacked_df.loc[index, 'Country_Name']
                    climbing_areas_df['State'] = stacked_df.loc[index, 'State']
                    climbing_areas_df['Region'] = stacked_df.loc[index, 'Region']
                    climbing_areas_df['Processed_Area_Description'] = processed_description
                    
                    # Append individual climbing area data to dfs_climbingareas
                    dfs_climbingareas.append(climbing_areas_df)
            except Exception as e:
                exception_list.append(e)
                print(f"Error processing task: {e}")
            
    # Shut down the executor
    executor.shutdown(wait=True)
    
    # Concatenate the dataframes
    climbingareas_df = pd.concat(dfs_climbingareas, ignore_index=True)
    
    climbingareas_df = climbingareas_df[['Continent_Name','Country_Name','State',
                                        'Region','Climbing_Area','Climbing_Area_Route_Count',
                                        'Processed_Area_Description']]

    
    climbingareas_df = perform_sentiment_analysis(climbingareas_df, description_column='Processed_Area_Description')
    
    # Filter out rows where Climbing_Area_Route_Count is not a digit or is 0
    climbingareas_df = climbingareas_df[climbingareas_df['Climbing_Area_Route_Count'].str.isdigit() & (climbingareas_df['Climbing_Area_Route_Count'].astype(int) > 0)]
    
    # Convert Climbing_Area_Route_Count to integer
    climbingareas_df['Climbing_Area_Route_Count'] = climbingareas_df['Climbing_Area_Route_Count'].astype(int)
    
    # Print exceptions with the dataframe
    error_tracking(exception_list, climbingareas_df)

# =============================================================================
# CLIMBING SECTION LOOP
# =============================================================================
    
    # Initialize Lists/Dictionarieis
    dfs_climbingsections = []
    exception_list = []
    future_to_url = {}

# =============================================================================
# Create data column to loop over
# =============================================================================
    # Create the URL column to iterate over
    climbingareas_df['URL'] = BASE_URL + '/' + climbingareas_df['Continent_Name'] + '/' + climbingareas_df['Country_Name']
    # Add State and Region if State is not NaN
    climbingareas_df.loc[climbingareas_df['State'].notna(), 'URL'] += '/' + climbingareas_df['State']
    climbingareas_df['URL'] += '/' + climbingareas_df['Region']
    # Add Climbing Area
    climbingareas_df['URL'] += '/' + climbingareas_df['Climbing_Area']
    # Apply URL encoding, excluding NaN values
    climbingareas_df['URL'] = climbingareas_df['URL'].apply(lambda x: encode_url(x) if pd.notna(x) else x)
    
    # Process URLs using concurrent futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        for index, row in climbingareas_df.iterrows():
            try:
                # Check if climbing_routes_list is empty
                if not row['Climbing_Area_Route_Count']:  
                    print(f"Skipping record with index {index} as it has no climbing routes.")
                    continue  
                # Construct the URL for the current row
                url = row['URL']
                # Submit task for the current URL
                future = executor.submit(extract_desired_section, url, "Climbing Sections:", index)  # Pass index here
                # Store the future in the dictionary
                future_to_url[future] = (index, url)
            except Exception as e:
                print(f"Error processing row {index}: {e}")
    
    # Iterate over completed tasks
        for future in concurrent.futures.as_completed(future_to_url):
            # Retrieve both index and URL associated with the future
            index, url = future_to_url[future]
            try:
                # Retrieve the result from the future
                climbing_sections_list, index, processed_description = future.result()
                
                if climbing_sections_list is not None:
                    # Append individual climbing area data to dfs_climbingsections
                    climbing_sections_df = pd.DataFrame(climbing_sections_list, columns=['Climbing_Section', 'Climbing_Section_Route_Count'])
                    climbing_sections_df['Continent_Name'] = climbingareas_df.loc[index, 'Continent_Name']
                    climbing_sections_df['Country_Name'] = climbingareas_df.loc[index, 'Country_Name']
                    climbing_sections_df['State'] = climbingareas_df.loc[index, 'State']
                    climbing_sections_df['Region'] = climbingareas_df.loc[index, 'Region']
                    climbing_sections_df['Climbing_Area'] = climbingareas_df.loc[index, 'Climbing_Area']
                    climbing_sections_df['Processed_Section_Description'] = processed_description
                    
                # Append individual climbing section data to dfs_climbingsections
                dfs_climbingsections.append(climbing_sections_df)
            except Exception as e:
                exception_list.append(e)
                print(f"Error processing task: {e}")
    
    # Shut down the executor
    executor.shutdown(wait=True)
    
    # Concatenate the dataframes
    climbingsections_df = pd.concat(dfs_climbingsections, ignore_index=True)
    
    climbingsections_df = climbingsections_df[['Continent_Name','Country_Name','State',
                                               'Region','Climbing_Area','Climbing_Section',
                                               'Climbing_Section_Route_Count',
                                               'Processed_Section_Description']]
    
    # # Applying the function to the Section_Description column and storing the results in a new column Processed_Section_Description    
    climbingsections_df = perform_sentiment_analysis(climbingsections_df, description_column='Processed_Section_Description')

    # Print exceptions with the dataframe
    error_tracking(exception_list, climbingsections_df)
        
    # Filter out non-numeric values in 'Climbing_Section_Route_Count'
    climbingsections_df = climbingsections_df[climbingsections_df['Climbing_Section_Route_Count'].str.isdigit()]
    
    # Convert Climbing_Section_Route_Count to integer
    climbingsections_df['Climbing_Section_Route_Count'] = climbingsections_df['Climbing_Section_Route_Count'].astype(int)
    
# =============================================================================
# ROUTE DETAILS LOOP
# =============================================================================
    
    # Initialize lists/Dictionaries
    dfs_routes = []
    exception_list = []
    future_to_url = {}
    
# =============================================================================
# Create data column to loop over
# =============================================================================

    # Create the URL column to iterate over
    climbingsections_df['URL'] = BASE_URL + '/' + climbingsections_df['Continent_Name'] + '/' + climbingsections_df['Country_Name']
    # Add State and Region if State is not NaN
    climbingsections_df.loc[climbingsections_df['State'].notna(), 'URL'] += '/' + climbingsections_df['State']
    climbingsections_df['URL'] += '/' + climbingsections_df['Region']
    # Add Climbing Area
    climbingsections_df['URL'] += '/' + climbingsections_df['Climbing_Area']
    # Add Climbing Section
    climbingsections_df['URL'] += '/' + climbingsections_df['Climbing_Section']
    
    # Apply URL encoding, excluding NaN values    
    climbingsections_df['URL'] = climbingsections_df['URL'].apply(lambda x: encode_url(x) if pd.notna(x) else x)
   
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        for index, row in climbingsections_df.iterrows():
            try:
                # Check if climbing_routes_list is empty
                if not row['Climbing_Section_Route_Count']:  # Assuming this column indicates the route count
                    print(f"Skipping record with index {index} as it has no climbing routes.")
                    continue  # Skip this record and move to the next one
                # Construct the URL for the current row
                url = row['URL']
                #print("Submitting URL:", url)  # Print the URL before submitting
                # Submit task for the current URL
                future = executor.submit(extract_climbing_route_details, row['URL'], index)
                # Store the future in the dictionary
                future_to_url[future] = (index, url)
            except Exception as e:
                print(f"Error processing row {index}: {e}")
    
        # Iterate over completed tasks
        for future in concurrent.futures.as_completed(future_to_url):
            index, url = future_to_url[future]
            try:
                climbing_routes_list, index = future.result()
                #print(climbing_routes_list)
                
                if climbing_routes_list is not None:
                    climbing_routes_df = pd.DataFrame(climbing_routes_list, columns=['Rock_Type', 'Climbing_Type', 'Rating', 'Difficulty', 'Ascents'])
                    climbing_routes_df['Continent_Name'] = climbingsections_df.loc[index, 'Continent_Name']
                    climbing_routes_df['Country_Name'] = climbingsections_df.loc[index, 'Country_Name']
                    climbing_routes_df['State'] = climbingsections_df.loc[index, 'State']
                    climbing_routes_df['Region'] = climbingsections_df.loc[index, 'Region']
                    climbing_routes_df['Climbing_Area'] = climbingsections_df.loc[index, 'Climbing_Area']
                    climbing_routes_df['Climbing_Section'] = climbingsections_df.loc[index, 'Climbing_Section']
                    climbing_routes_df['Climbing_Section_Route_Count'] = climbingsections_df.loc[index, 'Climbing_Section_Route_Count']
                    dfs_routes.append(climbing_routes_df)
            except ValueError as ve:
                print(f"Warning: Incomplete data for URL {url}: {ve}")
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
    
    # Shut down the executor
    executor.shutdown(wait=True)

    # Concatenate the dataframes
    climbingroutes_df = pd.concat(dfs_routes, ignore_index=True)
        
    # List all columns in the desired order
    new_order = ['Continent_Name','Country_Name','State','Region',
                'Climbing_Area','Climbing_Section','Climbing_Section_Route_Count']

    # Reorder the DataFrame columns
    climbingroutes_df = climbingroutes_df[new_order + [col for col in climbingroutes_df.columns if col not in new_order]]
    
    # Print exceptions with the dataframe
    error_tracking(exception_list, climbingroutes_df)
    
    # Convert Climbing_Section_Route_Count to integer
    climbingroutes_df['Climbing_Section_Route_Count'] = climbingroutes_df['Climbing_Section_Route_Count'].astype(int)

# =============================================================================
# Export data out to excel file
# =============================================================================

    # Create a Pandas Excel writer using xlsxwriter as the engine
    with pd.ExcelWriter('Route_Data.xlsx', engine='xlsxwriter', mode='w') as writer:
        # Write each DataFrame to a separate sheet
        continent_route_df.to_excel(writer, sheet_name='Continents')
        country_route_df.to_excel(writer, sheet_name='Countries')
        stacked_df.to_excel(writer, sheet_name='States_and_Regions')
        climbingareas_df.to_excel(writer, sheet_name='Climbing_Areas')
        climbingsections_df.to_excel(writer, sheet_name='Climbing_Sections')
        climbingroutes_df.to_excel(writer, sheet_name='Climbing_Routes')
        
    return continent_route_df, country_route_df, stacked_df, climbingareas_df, climbingsections_df, climbingroutes_df

#%% Executing Main Function To Gather Data

select_a_region('https://www.rockclimbing.com/routes')


    

    