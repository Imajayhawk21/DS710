#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 17:11:43 2024

@author: rajeshgogineni
"""

#%%

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
# Import necessary libraries for usage

# For mathematical calculations
import pandas as pd
import numpy as np

# For Plotting
import matplotlib.pyplot as plt

#%%
# =============================================================================
# Task 1.1
# Read in csv files into individual dataframes and then concatenate them together
# =============================================================================

def read_csv_files(filenames):
    
    # Empty dataframe initialized
    dataframes = {}
    
    for filename in filenames:
        
        # Extract a concise identifier from the filename if necessary
        identifier = filename.split('/')[-1].replace('.csv', '')
        
        # Read the CSV file and store it in the dictionary with the identifier as the key
        dataframes[identifier] = pd.read_csv(filename, low_memory=False)
    
    return dataframes

#%%
# Create dictionaries for each csv file

# File names in scope
filenames = ['1950.csv', '1960.csv', '1970.csv', '1973.csv', '1980.csv', '1990.csv', 
             '2000.csv', '2010.csv', '2020.csv']

# Combining dataframes into one dictionary, but still keeping them separate
dfs = read_csv_files(filenames)

#%%
# Concatenate all DataFrames in the dictionary into one

# Add a column 'source' to identify the original DataFrame each row came from
climate_df_all_source_include = pd.concat(
    [df.assign(source=filename) for filename, df in dfs.items()],
    ignore_index=True)

# Drop the 'source' column that I created for my own reference 
climate_df_all = climate_df_all_source_include.drop(columns=['source'])


#%%
# Test for concatenated dataframe

assert climate_df_all.shape==(709514, 124)

#%%
# =============================================================================
# Task 1.2
# Retain relevant columns and create new dataframe
# =============================================================================

# Columns to keep
columns_to_keep = ['STATION', 'DATE', 'REPORT_TYPE', 'SOURCE', 'DailyAverageWindSpeed', 
                   'DailyMaximumDryBulbTemperature', 'DailyMinimumDryBulbTemperature', 
                   'DailyPrecipitation', 'DailySnowDepth', 'DailySnowfall']

# Create a new DataFrame
climate_df = climate_df_all[columns_to_keep].copy()  

#%%
# Test for keeping only 10 columns

assert climate_df.shape==(709514, 10)

#%%
# =============================================================================
# Task 1.3.1
# Change variable to datetime for time series analysis
# =============================================================================

climate_df = climate_df.assign(DATE = pd.to_datetime(climate_df['DATE']))

#%%
# =============================================================================
# Task 1.3.2
# Clean up Report type column by stripping leading and trailing spaces
# =============================================================================

climate_df['REPORT_TYPE'] = climate_df['REPORT_TYPE'].str.strip()

#%%
# =============================================================================
# Task 1.3.3
# Modify DailyMaximumDryBulbTemperature, DailyMinimumDryBulbTemperature 
# to remove s and convert to float
# =============================================================================

def temp_converter(t):
    
    # Handles necessary dataframe manipulations
    if isinstance(t, pd.DataFrame):
        # Remove 's' character from both columns
        t = t.assign(DailyMaximumDryBulbTemperature=t['DailyMaximumDryBulbTemperature'].map(lambda x: str(x).replace('s', '') if isinstance(x, str) else x), 
                      DailyMinimumDryBulbTemperature=t['DailyMinimumDryBulbTemperature'].map(lambda x: str(x).replace('s', '') if isinstance(x, str) else x))
        
        # Convert string numbers to floats
        t = t.assign(DailyMaximumDryBulbTemperature=t['DailyMaximumDryBulbTemperature'].map(lambda x: float(x) if isinstance(x, str) and (x.isdigit() or (x[0] == '-' and x[1:].isdigit())) else x),
                      DailyMinimumDryBulbTemperature=t['DailyMinimumDryBulbTemperature'].map(lambda x: float(x) if isinstance(x, str) and (x.isdigit() or (x[0] == '-' and x[1:].isdigit())) else x))
        
        return t
    
    # Handles individuals strings for tests
    elif isinstance(t, str):
        t = str(t).replace('s', '')
        t = float(t)
        
        return t
    
    # If given an individual float then just returns the float
    else:
        return t



#%%
# Testing for Task 1.3.3

climate_df = temp_converter(climate_df)

#%%
# =============================================================================
# Task 1.3.4
# Task 1.3.5
# =============================================================================

def precip_converter(p):
    
    # Handles necessary dataframe manipulations
    if isinstance(p, pd.DataFrame):
        # Remove 's' character from both columns
        p = p.assign(DailyPrecipitation=p['DailyPrecipitation'].map(lambda x: str(x).replace('s', '') if isinstance(x, str) else x))
        
        # Replace T with 0.0001
        p = p.assign(DailyPrecipitation=p['DailyPrecipitation'].map(lambda x: str(x).replace('T', '0.0001') if isinstance(x, str) else x))
        p = p.assign(DailySnowDepth=p['DailySnowDepth'].map(lambda x: str(x).replace('T', '0.0001') if isinstance(x, str) else x))
        p = p.assign(DailySnowfall=p['DailySnowfall'].map(lambda x: str(x).replace('T', '0.0001') if isinstance(x, str) else x)) 
    
        # Convert string numbers to floats
        p = p.assign(DailyPrecipitation=p['DailyPrecipitation'].map(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else np.nan if isinstance(x, str) else x))
        p = p.assign(DailySnowDepth=p['DailySnowDepth'].map(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else np.nan if isinstance(x, str) else x))
        p = p.assign(DailySnowfall=p['DailySnowfall'].map(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else np.nan if isinstance(x, str) else x))
        
        return p 
    
    # Handles individuals strings for tests
    elif isinstance(p, str):
        if p == 'T':
            p = 0.0001
        else:
            p = str(p).replace('s', '')
            p = float(p)
            
        return p
    
    # If given an individual float then just returns the float
    else:
        return p

#%%

climate_df = precip_converter(climate_df)


#%%
# =============================================================================
# Task 1.3.6 
# Assert statements to check column and make sure that they convert correctly
# =============================================================================

# Columns that we are confirming dtype
# =============================================================================
# column name	                    expected type
# STATION	                        int64
# DATE	                            datetime64[ns]
# REPORT_TYPE	                    object
# SOURCE	                        object
# DailyAverageWindSpeed	            float64
# DailyMaximumDryBulbTemperature	float64
# DailyMinimumDryBulbTemperature	float64
# DailyPrecipitation	            float64
# DailySnowDepth	                float64
# DailySnowfall	                    float64
# =============================================================================


# Check integer types
assert climate_df['STATION'].dtype == 'int64', f"Expected {'STATION'} to be {'int64'}, got {climate_df['STATION'].dtype}"

# Check datetime types
assert climate_df['DATE'].dtype == 'datetime64[ns]', f"Expected {'DATE'} to be {'datetime64[ns]'}, got {climate_df['DATE'].dtype}"

# Check string types
assert climate_df['REPORT_TYPE'].dtype == 'object', f"Expected {'REPORT_TYPE'} to be {'object'}, got {climate_df['REPORT_TYPE'].dtype}"
assert climate_df['SOURCE'].dtype == 'object', f"Expected {'SOURCE'} to be {'object'}, got {climate_df['SOURCE'].dtype}"

# Check float types
assert climate_df['DailyAverageWindSpeed'].dtype == 'float64', f"Expected {'DailyAverageWindSpeed'} to be {'float64'}, got {climate_df['DailyAverageWindSpeed'].dtype}"
assert climate_df['DailyMaximumDryBulbTemperature'].dtype == 'float64', f"Expected {'DailyMaximumDryBulbTemperature'} to be {'float64'}, got {climate_df['DailyMaximumDryBulbTemperature'].dtype}"
assert climate_df['DailyMinimumDryBulbTemperature'].dtype == 'float64', f"Expected {'DailyMinimumDryBulbTemperature'} to be {'float64'}, got {climate_df['DailyMinimumDryBulbTemperature'].dtype}"
assert climate_df['DailyPrecipitation'].dtype == 'float64', f"Expected {'DailyPrecipitation'} to be {'float64'}, got {climate_df['DailyPrecipitation'].dtype}"
assert climate_df['DailySnowDepth'].dtype == 'float64', f"Expected {'DailySnowDepth'} to be {'float64'}, got {climate_df['DailySnowDepth'].dtype}"
assert climate_df['DailySnowfall'].dtype == 'float64', f"Expected {'DailySnowfall'} to be {'float64'}, got {climate_df['DailySnowfall'].dtype}"

#%%
# =============================================================================
# Task 2.1
# Filter report by SOD and check expected shape
# =============================================================================

daily_df = climate_df[climate_df['REPORT_TYPE'] == 'SOD']

assert daily_df.shape[0] == 9473

#%%
# =============================================================================
# Task 2.2
# Plot Daily Snow Depth Over Time
# =============================================================================

def daily_snow_depth(df):
    
    # Created a Figure object
    fig = plt.figure()

    # Plot x and y variables in this order in a line graph
    plt.plot(df['DATE'], df['DailySnowDepth'])

    # Added labels and title
    plt.xlabel('Year')
    plt.ylabel('Daily Snow Depth (in inches)')
    plt.title('Daily Snow Depth Over Time')

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_assign6c_task2-1.png')
            
    return      

#%%
# Create line plot and save it for task 2.2

daily_snow_depth(daily_df)

#%%
# =============================================================================
# Task 2.3.1
# Take values from column and determine which year the date falls into 
# You can do this with the month and add 1 if it is July or more
# =============================================================================

def winter_bin(d):
  
    # Extract month from the datetime object, check if input is a dataframe
    # Apply a lambda function to apply to each row
    if isinstance(d, pd.DataFrame):
        # Apply the lambda function output to each row and create a new column 
        mapping = lambda row: row['DATE'].year + 1 if row['DATE'].month >= 7 else row['DATE'].year
        d = d.assign(WINTER=d.apply(mapping, axis=1))     
        return d
        
    # Check if the input is a single datetime value
    elif isinstance(d, pd.Timestamp):
        # Apply the mapping function to the single datetime value
        return d.year + 1 if d.month >= 7 else d.year
    
    else:
        raise ValueError("Input must be a DataFrame or a single datetime value")

    
#%%
# Add WINTER column on to dataframe

daily_df = winter_bin(daily_df)

#%%
# Tests to check winter_bin is working or not

assert winter_bin(pd.to_datetime('1995-06-01 23:59:00')) == 1995
assert winter_bin(pd.to_datetime('1995-07-01 23:59:00')) == 1996

#%%
# =============================================================================
# Task 2.3.2
# Find Max of Daily Snow Depth for each winter season
# =============================================================================

max_daily_snowfall = daily_df.pivot(columns=['WINTER']).DailySnowDepth.max()

#%%
# Tests for 2.3.2

assert max_daily_snowfall.shape == (27,)
assert max_daily_snowfall.loc[2019] == 25.0

#%%
# =============================================================================
# Task 2.3.3
# Plot line graph for max daily snowfall
# =============================================================================

def max_snow_fall_visual(df):
    
    # Created a Figure object
    fig = plt.figure()

    # Plot x and y variables in this order in a line graph
    plt.plot(max_daily_snowfall.index, max_daily_snowfall.values)

    # Added labels and title
    plt.xlabel('Winter')
    plt.ylabel('Max Daily Snowfall (in inches)')
    plt.title('Max Daily Snowfall Each Winter')

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_assign6c_task2-3.png')
            
    return      

#%%
# Create line plot and save it for task 2.2

max_snow_fall_visual(max_daily_snowfall)

#%%
# =============================================================================
# Task 2.4
# 🎯 Use a pivot table on YEAR, and sum the DailyPrecipitation column. 
# Store the result in a variable called yearly_precipitation. 
# The resulting variable should be a Series, with index column as YEAR.
# =============================================================================

# Extract year 
daily_df['YEAR'] = daily_df['DATE'].map(lambda x: x.year)

# Find max precipitation in a calendar year and drop NaN
yearly_precipitation = daily_df.pivot(columns=['YEAR']).DailyPrecipitation.sum().dropna()

#%%
# Plot precipitation over a calendar year

def total_precipation_visual(df):
    
    # Created a Figure object
    fig = plt.figure()

    # Plot x and y variables as a bar graph
    plt.bar(yearly_precipitation.index, yearly_precipitation.values)

    # Added labels and title
    plt.xlabel('Year')
    plt.ylabel('Total Precipation (in inches)')
    plt.title('Total Precipation Each Year')

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_assign6c_task2-4.png')
            
    return      

#%%
# Create bar graph and save it for task 2.4

total_precipation_visual(yearly_precipitation)

#%%
# =============================================================================
# Task 3.3
# 🎯 Write a function read_fine_foods(filename) to use text processing, 
# control flow, 
# and built-in Python collections 
# to read a file of identical structure into memory.
# =============================================================================

def read_fine_foods(filename):

    # Initialize an empty list to store dictionaries
    data = []

# =============================================================================
# 'productId' -- the Product IDs
# 'userId -- the user's id
# 'profileName' -- the profile name for the person leaving the review
# 'helpfulness' -- the string, with /, for the number of votes for whether the review was helpful
# 'score' -- the reviewer's rating of the product. This must be a float.
# 'summary' -- the short summary of the review
# 'text' -- the text of the review (you will drop this before writing the data to a csv)
# =============================================================================
    
    column_map = {
        'product/productId': 'productId',
        'review/userId': 'userId',
        'review/profileName': 'profileName',
        'review/helpfulness': 'helpfulness',
        'review/time': 'time',
        'review/score': 'score',
        'review/summary': 'summary',
        'review/text': 'text'}

    # Open the text file and iterate through each line
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        
        # Initialize empty dictionary
        current_record = {}
        
        for line in file:
            # Check if the line is empty, indicating the end of a record
            if line.strip() == '':
                if current_record:
                    # Add the current record to the list
                    data.append(current_record)
                    # Start a new record
                    current_record = {}
                    
            else:
                # Split each line by the colon (':') character
                parts = line.strip().split(': ', 1)
                if len(parts) == 2:
                    key, value = parts
                    # Add key-value pair to the current record
                    current_record[key] = value
                else:
                    # Handle lines with unexpected format
                    value = np.nan

        # Add the last record to the list (if any)
        if current_record:
            data.append(current_record)

    # Create a DataFrame from the list of dictionaries and modify it
    df = pd.DataFrame(data)
    
    # Change column names
    df = df.rename(columns=column_map)
        
    # Clean up specific dataframe columns
    df['score'] = df['score'].astype(float)

    return df

#%%
# =============================================================================
# Task 3.6
# The index of the resulting dataframe is
# 'productID' - The product ID's, there should be no duplicates here.
#
# These are the columns in the new dataframe:
# 'numReviews' - The number of reviews in product_df of the given product
# 'averageScore' - the mean value of the ratings for the given product
# 'num5' - the number of reviews that gave the product a score of 5.0
# 'num4' - the number of reviews that gave the product a score of 4.0
# 'num3' - the number of reviews that gave the product a score of 3.0
# 'num2' - the number of reviews that gave the product a score of 2.0
# 'num1' - the number of reviews that gave the product a score of 1.0
# =============================================================================


#%%

def analyze_by_product(df):
        
    # Create an empty dataframe with the index
    product_df = pd.DataFrame(index=df['productId'].unique())
        
    # Calculate average by productId and add to product_df
    mean_by_productId = df.groupby('productId')['score'].mean()
    product_df['averageScore'] = mean_by_productId    
        
    # Group by productId and score, then count the occurrences
    score_counts = df.groupby(['productId', 'score']).size().unstack(fill_value=0)
    
    # Merge the counts back into the original DataFrame
    product_df = product_df.merge(score_counts, left_index=True, right_index=True, how='left')
    
    # Rename the columns 
    product_df.rename(columns={5.0: 'num5', 4.0: 'num4', 3.0: 'num3', 2.0: 'num2', 1.0: 'num1'}, inplace=True)

    # Create numReviews column and fill NaN with 0 and make these integer columns
    # product_df['num5']=product_df['num5'].fillna(0).astype(int)
    # product_df['num4']=product_df['num4'].fillna(0).astype(int)
    # product_df['num3']=product_df['num3'].fillna(0).astype(int)
    # product_df['num2']=product_df['num2'].fillna(0).astype(int)
    # product_df['num1']=product_df['num1'].fillna(0).astype(int)

    product_df['numReviews']=product_df['num5']+product_df['num4']+product_df['num3']+product_df['num2']+product_df['num1']
    
# =============================================================================
# Recommendation score
#
# A weighted average will allow us to handle distribution of reviews and amount
# =============================================================================

    total_reviews = product_df['numReviews'].sum()    
    normalized_counts = product_df[['num5', 'num4', 'num3', 'num2', 'num1']].div(total_reviews, axis=0).fillna(0)
     
    # Calculate the weighted sum of scores
    weighted_sum = (product_df['averageScore'] * normalized_counts['num5'] +
                    product_df['averageScore'] * normalized_counts['num4'] +
                    product_df['averageScore'] * normalized_counts['num3'] +
                    product_df['averageScore'] * normalized_counts['num2'] +
                    product_df['averageScore'] * normalized_counts['num1'])
    
    # Calculate the weighted average score
    product_df['recommendationScore'] = (weighted_sum / total_reviews)
    
    return product_df

#%%
# =============================================================================
# Task 3.4    
# In process_foods(filename), write code to add a column to amazon_df:
# 
# 'reviewLength' -- length of the review's text
# =============================================================================

def process_foods(filename):

    # Create initial amazon review dataframe
    amazon_df = read_fine_foods(filename)
    
    # Split the values in 'column' by the backslash and expand them into separate columns
    amazon_df[['numVotesHelpful', 'numVotesTotal']] = amazon_df['helpfulness'].str.split('/', expand=True)
    
    # Convert the values in the new columns to integers
    amazon_df['numVotesHelpful'] = amazon_df['numVotesHelpful'].astype(int)
    amazon_df['numVotesTotal'] = amazon_df['numVotesTotal'].astype(int)

    # Lambda function that assigns NaN when both columns or zero
    # Calculates a score when both columns are not zero
    amazon_df = amazon_df.assign(reviewHelpfulnessScore=amazon_df.apply(lambda row: np.nan if row['numVotesHelpful'] == 0 and row['numVotesTotal'] == 0 
                                                                        else (row['numVotesHelpful']/row['numVotesTotal']), axis=1))

# =============================================================================
# Task 3.5
# In process_foods(filename), write code to add a column to amazon_df:
# 
# 'hasColonInText' -- True if the text has a colon : in it, and False if not.
# =============================================================================
    
    # Remove the leading and trailing spaces then count the length of the characters
    amazon_df = amazon_df.assign(reviewLength=amazon_df['text'].str.strip().apply(len))
    
    # Check if new column has a : in it
    amazon_df = amazon_df.assign(hasColonInText=amazon_df['text'].astype(str).str.contains(':'))


# =============================================================================
# Task 3.6 Execution within process_foods function
# =============================================================================

    product_df = analyze_by_product(amazon_df)
        
# =============================================================================
# Task 3.8
#
# Output CSV file, drop indices, handle NaN values 
# =============================================================================
    
    amazon_df_copy = amazon_df.reset_index(drop=True).drop(columns=['text'])
    amazon_df_copy.to_csv('all_foods_reviews.csv', sep=',', index=False, na_rep='NA')
    
    product_df_copy = product_df.reset_index(drop=True)
    product_df_copy.to_csv('product_review_data.csv', sep=',', index=False)
    
    return amazon_df, product_df

#%%
# =============================================================================
# Task 3.7
#
# num_reviews -- How many reviews are in the data set df?
# avg_length -- What is the average length of a review's text (in characters) in df?
# num_reviews_with_colon -- How many reviews in df contain a ':'?
# most_reviewed_id -- What is the productId of the item with the most number of reviews? By reviews I mean the number of times the particular "food" appears in the data set. This does not refer to helpfulness ratings. (🧠 Let's assume that only one most common item exists, for the sake of this exercise. How would your code change if multiple items tied for most reviews, and in this case what type do you think would be best for most_reviewed_id?)
# times_most_reviewed -- The number of times the most-reviewed product was reviewed, in this data frame df. (🧠 again, how would this change if we allowed ties?)
# =============================================================================

def summary_stats(df):
        
    # Initialize empty dictionary
    sum_stats ={}
    
    # Get size of the dataframe
    sum_stats['num_reviews'] = len(df)
    
    # Average Length of a review 
    sum_stats['avg_length'] = df['reviewLength'].mean()

    # Calculating a count of reviews with a colon in the text
    contains_colon = df['text'].astype(str).str.contains(':')
    sum_stats['num_reviews_with_colon'] = contains_colon.sum()
    
    # Most reviewed productId
    counts = df.groupby('productId').size() # Group By Product Id and get the size of each of them
    max_count = counts.max()  # Find the maximum count
    productId_with_max_count = counts[counts == max_count].index.tolist()  # Get all values with the maximum count
    sum_stats['most_reviewed_id'] = productId_with_max_count # Insert into dictionary
    
    # The integer value for the max count of reviews
    sum_stats['times_most_reviewed'] = max_count
    
    return sum_stats

#%%
# inside the `if` is guarded code that doesn't run if the script is imported into another script
if __name__ == "__main__": 
    amazon_df, product_df = process_foods('finefoods_excerpts.txt')
    print(summary_stats(amazon_df)) # call function from task 3.7
    #print(product_df)

    


