#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:04:39 2024

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
# =============================================================================
# Task 1.1
# =============================================================================

# Open the JSON file
with open("english_letter_scores.json", "r") as file_eng:
    # Load the JSON data into a Python dictionary
    english_letter_scores = json.load(file_eng)    
    english_letter_scores = {int(key): value for key, value in english_letter_scores.items()}
    
# Open the JSON file
with open("german_letter_scores.json", "r") as file_ger:
    # Load the JSON data into a Python dictionary
    german_letter_scores = json.load(file_ger)
    german_letter_scores = {int(key): value for key, value in german_letter_scores.items()}

    
#%%

def word_score(word, score_dict):
    
    # Initialize total_score
    total_scor= 0
    
    # Capitalize word after taking value in
    word = word.upper()
    
    # Iterate over each letter in the word
    for letter in word:
        
        # Initialize letter_found
        letter_found = False
        
        # Iterate over each key-value pair in the dictionary
        for key, values in score_dict.items():
            
            # Check if the letter is in the values corresponding to the key
            if letter in values:
                
                # Add the key to the total score
                total_score += key
                
                # letter is in the dictionary
                letter_found = True
                break
        
        if not letter_found:
            total_score = np.nan
            break

    return total_score

#%%

word_score("FOX",english_letter_scores) == 13
word_score("FOX",german_letter_scores) == 14
np.isnan(word_score("FÖX",english_letter_scores)) == True

#%%
# =============================================================================
# Functions needed to accomplish Task 1.2
# =============================================================================

#This function will check if we are receiving a string in general and/or for the filename 
#If we do not then it will throw a type error

def invalid_input(xx):
    if isinstance(xx, str) == False and xx is not None:
        raise TypeError('An argument should be a string. Please try again.')
        return None,None 

#%%
#Function that returns all non alphabetic characters from a string

def non_alpha_chars(s):
    
    #Establish string value to add to    
    non_alphabetic_chars = ''
    for char in s:
        if not char.isalpha():
            non_alphabetic_chars += char
    return set(non_alphabetic_chars)
    
#%%
# Function that returns all non space characters from a string

def non_space_chars(s):
    
    #Establish string value to add to    
    non_space_chars = ''
    
    for char in s:
        if not char.isspace():
            non_space_chars += char
    return set(non_space_chars)


#%%
# Combine non_alpha and non_space functions together.
# This is a nested function

def non_alpha_non_space_chars(s):
    
    invalid_input(s)
    
    combined_set = non_space_chars(non_alpha_chars(s))    
    
    return combined_set 

#%%
# Clean function that returns all the letters and makes them lowercase for the entire input file

def read_and_clean(filename):
    #read txt file into memory and create variable
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        
        combined_set = non_alpha_non_space_chars(text)
        
        new_text =''
        
        for char in text:
            if char not in combined_set:
                new_text += char
            
        return new_text.lower()
    
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")


#%%
# =============================================================================
# Task 1.2
# =============================================================================

#Word count of contents of a file
def word_counts_from_file(filename):
    
    # Split the input file contents
    filtered_split_filename = read_and_clean(filename).split()

    # Initialize the dictionary for counting of words
    filename_contents_word_count = {}
    
    # oop to count each word and increment words against the key
    for word in filtered_split_filename:
        # If the word is already in the dictionary, increment its count
        if word in filename_contents_word_count:
            filename_contents_word_count[word] += 1
        # If the word is not in the dictionary, add it with count 1
        else:
            filename_contents_word_count[word] = 1
    
    
    # Convert dictionary into DataFrame
    word_counts_df = pd.DataFrame.from_dict(filename_contents_word_count, orient='index')
    
    # Name Count column and reset index for word Column
    word_counts_df.columns = ['Count']
    word_counts_df.reset_index(inplace=True)

    # Name Word column 
    word_counts_df.rename(columns={'index':'Word'}, inplace=True)
        
    return word_counts_df
    
#%%
# Setting as global variable for later use

word_counts_df = word_counts_from_file('example_text.txt')

#%%

def add_score_column(df, score_dict, new_column_name):
    
    # Apply the function to create a new column indicating if the value is a conjunction
    df[new_column_name] = df['Word'].apply(lambda x: word_score(x, score_dict))
    
    return None

#%%
# =============================================================================
# Task 1.3
# =============================================================================

def score_data(df, count_column, score_column, ignored_words = []):    
    
    # Remove NaN values from counts to calculate correct average
    df = df.dropna()
    
    # Remove observations where 'Word' is in the list of values to remove
    df = df[~df['Word'].isin(ignored_words)]
    
    # Desired Descriptive Statistics
    sum_score = (df[count_column] * df[score_column]).sum()    
    avg_score = (sum_score/(df[count_column].sum()))
    expanded_scores = df[score_column].repeat(df[count_column])
    median_score = expanded_scores.median()

    return sum_score, avg_score, median_score


#%%

df = word_counts_from_file("example_text.txt")
add_score_column(df,english_letter_scores,"English Score")
add_score_column(df,german_letter_scores,"German Score")
assert score_data(df,"Count","English Score") == (319, 6.018867924528302, 7.0)
assert score_data(df,"Count","German Score") == (312.0, 5.886792452830188, 5.0)


#%%
# =============================================================================
# Task 1.4
# =============================================================================

# stopwords for both english and german, so we can remove these from analysis later
stopwords_english = nltk.corpus.stopwords.words('english')
stopwords_german = nltk.corpus.stopwords.words('german')

score_data(df,"Count","English Score",stopwords_english) == (193.0, 9.19047619047619, 10.0)

#%%
# =============================================================================
# Task 2.1
# =============================================================================

def wikipedia_page_content(title):
    
    response = requests.get(
    'https://en.wikipedia.org/w/api.php', # The wikipedia api tool
    params={
        'action': 'query', 
        'format': 'json', # Creates a container of collections 
        'titles': title , # Title of the Wikipedia Page
        'prop': 'extracts', # Use the TextExtracts extension to actually get the text
        # 'exintro': True, # Restricts pull to the content before the first header, we don't want this
        'explaintext': True, # Response returns plain text only
     }
 ).json()

    # Select the wikipedia page
    page = next(iter(response['query']['pages'].values()))

    # Select the content of the page
    text = page['extract']
       
    return text

#%%

assert wikipedia_page_content('Carla Cotwright-Williams')[:287] == "Carla Denise Cotwright-Williams (born November 6) is an American mathematician who works as a Technical Director and Data Scientist for the United States Department of Defense. She was the second African-American woman to earn a doctorate in mathematics at the University of Mississippi."

#%%
# =============================================================================
# Task 2.2
# =============================================================================

# Create object from the selected url
url_interstates = 'https://en.wikipedia.org/wiki/List_of_Interstate_Highways'
response_interstates = requests.get(url_interstates)

#%%

# Parse the HTML content using BeautifulSoup
soup_interstates = BeautifulSoup(response_interstates.content, features="lxml")

# Find all relevant tables in the HTML content
tables_interstate = soup_interstates.find_all('table', {'class', 'wikitable'})

#%%
# Getting embedded interstate/highway title

#Initialize list 
table_data_title = []

for table in tables_interstate:
    
    # Extract the data from each row (tr = table row) 
    rows = table.find_all('tr')
    
    # Initialize list
    table_rows = []
    
    for row in rows:
        # Check if 'th' element exists in the row
        th_element = row.find('th')
        
        if th_element:
            # Check if 'a' tag exists within 'th' element
            a_tag = th_element.find('a')
            
            if a_tag:
                # Extract the 'title' attribute
                cells = a_tag.attrs.get('title', '')
                
                # Initalize list
                row_data = []
                
                # Append the string 'cells' as a single element list
                row_data.append(cells)  
                
                # Append the row data to table_rows
                table_rows.append(row_data)  
    
    table_data_title.append(table_rows)

flattened_list = [item for sublist in table_data_title for item in sublist]
formatted_list = [item[0] for item in flattened_list]

#%%
# Getting year that this was formed

table_data_formed = []

# Iterate through each table in tables_interstate
for table in tables_interstate:
    # Find all rows in the current table
    rows = table.find_all('tr')

    # Iterate through each row in the table
    for row in rows[1:-1]:
        # Find all cells in the current row
        cells = row.find_all('td')
        
        # Check if the row contains at least 5 cells before accessing the fifth cell
        if len(cells) >= 5:
            
            # Extract the text from the fifth column and take the last 4 characters
            cell_text = cells[4].get_text().strip()[-4:]
            
            # Append the extracted text to the list
            table_data_formed.append(cell_text)
            
        else:
            # Handle the case where the row doesn't have enough cells
            table_data_formed.append(np.nan)

# Initialize list
converted_list = []

# Convert to integer or NaN
for item in table_data_formed:
    try:
        converted_list.append(int(item))
    except ValueError:
        converted_list.append(np.nan)

#%%
# Getting length in miles of the interstate or highway

table_data_length = []

# Iterate through each table in tables_interstate
for table in tables_interstate:
    # Find all rows in the current table
    rows = table.find_all('tr')

    # Iterate through each row in the table
    for row in rows[1:-1]:
        # Find all cells in the current row
        cells = row.find_all('td')
        
        # Check if the row contains at least 5 cells before accessing the fifth cell
        if len(cells) >= 5:
            # Extract the text from first column and take the last 8 characters
            
            cell_text = cells[0].get_text().strip()[-8:]
            
            # Append the extracted text to the list
            table_data_length.append(cell_text)
            
        else:
            # Handle the case where the row doesn't have enough cells
            table_data_length.append(np.nan)
            
# Initialize list
cleaned_list = []

# Convert to float or NaN
for x in table_data_length:
    try:
        cleaned_list.append(float(x))
    except ValueError:
        cleaned_list.append(np.nan)

#%%
# Getting embedded state for southern and western terminus

table_data_southern_western_terminus = []

# Iterate through each table in tables_interstate
for table in tables_interstate:
    # Find all rows in the current table
    rows = table.find_all('tr')

    # Iterate through each row in the table
    for row in rows[1:-1]:
        # Find all cells in the current row
        cells = row.find_all('td')
        
        # Check if the row contains at least 5 cells before accessing the fifth cell
        if len(cells) >= 5:
            # Get the text from column number 2 and strip it by 15 space from the end
            cell = cells[2].get_text().strip()[-15:]

            # Capitalize the extracted cell
            capitalized_cell = cell.upper().strip()
            
            # Add to list
            table_data_southern_western_terminus.append(capitalized_cell)
            
            # Clean up list
            table_data_southern_western_terminus = [s.split()[-1] for s in table_data_southern_western_terminus]
        else:
            # Handle the case where the row doesn't have enough cells
            table_data_southern_western_terminus.append(np.nan)

#%%
# Getting embedded state for northern and eastern terminus

table_data_northern_eastern_terminus = []

# Iterate through each table in tables_interstate
for table in tables_interstate:
    # Find all rows in the current table
    rows = table.find_all('tr')

    # Iterate through each row in the table
    for row in rows[1:-1]:
        # Find all cells in the current row
        cells = row.find_all('td')
        
        # Check if the row contains at least 5 cells before accessing the fifth cell
        if len(cells) >= 5:
            # Get the text from column number 3 and strip it by 15 space from the end
            cell = cells[3].get_text().strip()[-15:]

            # Capitalize the extracted cell
            capitalized_cell = cell.upper().strip()
            
            # Add to list 
            table_data_northern_eastern_terminus.append(capitalized_cell)
            
            # Clean up list
            table_data_northern_eastern_terminus = [s.split()[-1] for s in table_data_northern_eastern_terminus]
        else:
            # Handle the case where the row doesn't have enough cells
            table_data_northern_eastern_terminus.append(np.nan)

#%%

# Combine the lists into a single list of tuples
combined_data = list(zip(formatted_list, cleaned_list, converted_list))
combined_data_all_columns = list(zip(formatted_list, cleaned_list, converted_list, table_data_southern_western_terminus, table_data_northern_eastern_terminus))

# Create a DataFrame for interstate
interstate_df = pd.DataFrame(combined_data, columns=['Title', 'Length(mi)', 'Formed'])

# Create a DataFrame for more columns to be included
all_columns_interstate_df = pd.DataFrame(combined_data_all_columns, columns=['Title', 'Length(mi)', 'Formed', 'Southern Western Terminus State', 'Northern Eastern Terminus State'])
#%%
# Tests on interstate dataframe

assert "Interstate 2" in list(interstate_df["Title"])
assert "Interstate H-1" in list(interstate_df["Title"])
assert "Interstate A-1" in list(interstate_df["Title"])
assert "Puerto Rico Highway 1" in list(interstate_df["Title"])

#%%
# Applying the function to each element in Title and store the results in Page Contents

interstate_df['Page Contents'] = interstate_df['Title'].apply(lambda x: wikipedia_page_content(x))
all_columns_interstate_df['Page Contents'] = all_columns_interstate_df['Title'].apply(lambda x: wikipedia_page_content(x))

    
#%%
# =============================================================================
# Task 2.3
# =============================================================================

# Function to remove stopwords

def remove_stopwords(text):
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Remove stopwords from the words
    filtered_words = [word for word in words if word.lower() not in stopwords_english]
    
    # Join the remaining words back into a string
    processed_text = ' '.join(filtered_words)
    
    return processed_text

# Applying the function to the Page Contents column and store the results in a new column Processed Page Contents
interstate_df['Processed Page Contents'] = interstate_df['Page Contents'].apply(remove_stopwords)
all_columns_interstate_df['Processed Page Contents'] = all_columns_interstate_df['Page Contents'].apply(remove_stopwords)

#%%

# Initialize the SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# Applying sid for sentiment analysis and creating four new columns from it
interstate_df[['neg', 'neu', 'pos', 'compound']] = interstate_df['Processed Page Contents'].apply(lambda x: pd.Series(sid.polarity_scores(x)))
all_columns_interstate_df[['neg', 'neu', 'pos', 'compound']] = all_columns_interstate_df['Processed Page Contents'].apply(lambda x: pd.Series(sid.polarity_scores(x)))

#%%
# =============================================================================
# Task 2.4
# =============================================================================

def compound_variable_relationship(df, x, c, task):
    
    # Created a Figure object
    fig = plt.figure()

    # Use Seaborn library to put markers on scatterplot
    sns.scatterplot(data=df, x=x, y=c)

    # Added labels and title
    plt.xlabel(x)
    plt.ylabel('Sentiment Score')
    plt.title('How A Variable Impacts Sentiment Towards Interstates/Highways')
    plt.grid(True)

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_assign8_' + task)
            
    return    

#%%
# Create scatterplot and save it for task 2.4

compound_variable_relationship(interstate_df, x = 'Length(mi)', c = 'compound', task = 'task2-4.png')

#%%
# =============================================================================
# Task 2.5
# =============================================================================
# Create scatterplot and save it for task 2.5

compound_variable_relationship(interstate_df, x = 'Formed', c = 'compound', task = 'task2-5.png')

#%%
# =============================================================================
# Task 2.6
# =============================================================================

# I am going to modify the interstates dataframe to create a categorical variable.
# This variable will be match or no match based on if the south terminus and 
# north terminus are the same or different

# Compare the two columns and create a new column indicating match or no match
all_columns_interstate_df['Comparison'] = all_columns_interstate_df.apply(lambda row: 'Match' if row['Southern Western Terminus State'] == row['Northern Eastern Terminus State'] else 'No Match', axis=1)

#%%

def compound_variable_relationship(df, x, c, task):
    
    # Created a Figure object
    fig = plt.figure(figsize=(10,10))

    # Use Seaborn library plot a boxplot
    sns.boxplot(data=df, x=x, y=c)

    # Added labels and title
    plt.xlabel(x)
    plt.ylabel('Sentiment Score')
    plt.title('How A Variable Impacts Sentiment Towards Interstates/Highways')
    plt.grid(True)

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_assign8_' + task)
            
    return    

#%%
# Create scatterplot and save it for task 2.5

compound_variable_relationship(all_columns_interstate_df, x = 'Comparison', c = 'compound', task = 'task2-6.png')


