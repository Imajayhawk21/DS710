#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:22:27 2024

@author: rajeshgogineni
"""

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
# Import necessary libraries for usage

# For mathematical calculations
import pandas as pd

# For Plotting
import matplotlib.pyplot as plt
import seaborn as sns

# For Exporting
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

#%% Reading in excel file into dataframes

dfs = {}

sheet_names = ['Continents', 
               'Countries', 
               'States_and_Regions', 
               'Climbing_Areas', 
               'Climbing_Sections',
               'Climbing_Routes'
               ]

for sheet_name in sheet_names:
    try:
        dfs[sheet_name] = pd.read_excel('Route_Data.xlsx', sheet_name=sheet_name)
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
    except Exception as e:
        print("An error occurred while reading the Excel file:", e)
    
continents_df = dfs['Continents']
countries_df = dfs['Countries']
states_and_regions_df = dfs['States_and_Regions']
climbing_areas_df = dfs['Climbing_Areas']
climbing_sections_df = dfs['Climbing_Sections']
routes_df = dfs['Climbing_Routes']

#%% General Statistics

# =============================================================================
# What parts of the world have the most amount of routes? Done
# How many routes out of the total actually have ratings? Done, just need to summarize
# What is the average rating for a route that does get rated? Done
# What does the breakdown of type of climbing look like? Done
# What kind of rock exists across the world? Done
# =============================================================================

#%% Creation of data 

# Mapping for Route Difficulty
difficulty_map = {
    '5.15d': 'hard','5.15c': 'hard','5.15b': 'hard','5.15a': 'hard','5.15':  'hard',
    '5.14d': 'hard','5.14c': 'hard','5.14b': 'hard','5.14a': 'hard','5.14':  'hard',
    '5.13d': 'hard','5.13c': 'hard','5.13b': 'hard','5.13a': 'hard','5.13':  'hard',
    '5.12d': 'hard','5.12c': 'hard','5.12b': 'hard','5.12a': 'hard','5.12':  'hard',
    '5.11d': 'hard','5.11c': 'hard','5.11b': 'hard','5.11a': 'hard','5.11':  'hard',
    '5.10d': 'medium','5.10c': 'medium','5.10b': 'medium','5.10a': 'medium','5.10':  'medium',
    '5.9d': 'medium','5.9c': 'medium','5.9b': 'medium','5.9a': 'medium','5.9':  'medium',
    '5.8d': 'medium','5.8c': 'medium','5.8b': 'medium','5.8a': 'medium','5.8':  'medium',
    '5.7d': 'medium','5.7c': 'medium','5.7b': 'medium','5.7a': 'medium','5.7':  'medium',
    '5.6d': 'easy','5.6c': 'easy','5.6b': 'easy','5.6a': 'easy','5.6':  'easy',
    '5.5d': 'easy','5.5c': 'easy','5.5b': 'easy','5.5a': 'easy','5.5':  'easy',
    '5.4d': 'easy','5.4c': 'easy','5.4b': 'easy','5.4a': 'easy','5.4':  'easy',
    '5.3d': 'easy','5.3c': 'easy','5.3b': 'easy','5.3a': 'easy','5.3':  'easy'
    }

v_scale_map = {
    'V0': 'easy','V1': 'easy','V2': 'easy',
    'V3': 'medium','V4': 'medium','V5': 'medium',
    'V6': 'hard','V7': 'hard','V8': 'hard',
    'V9': 'hard','V10': 'hard','V11': 'hard',
    'V12': 'hard','V13': 'hard','V14': 'hard',
    'V15': 'hard','V16': 'hard','V17': 'hard'
}

routes_df['Difficulty_Level'] = routes_df['Difficulty'].map(difficulty_map)
routes_df['Difficulty_Level'] = routes_df['Difficulty_Level'].combine_first(routes_df['Difficulty'].map(v_scale_map))

#%% Function for General Statistics Visualization to Understand Data Patterns

# =============================================================================
# Statistics
# =============================================================================

def general_climbing_stats_routes(df):
    
    rating_counts = df['Rating'].value_counts()
    rating_counts_df = rating_counts.reset_index()
    rating_counts_df.columns = ['Average_Rating', 'Count']
    rating_counts_df = rating_counts_df[rating_counts_df['Average_Rating'] > 0]
    
    total_count_rating = rating_counts_df['Count'].sum()

    # Calculate the percentage for each row
    rating_counts_df['Percentage_of_Counts'] = round(((rating_counts_df['Count'] / total_count_rating) * 100),2)
    
    sum_of_rating_counts = rating_counts_df['Count'].sum()
    total_rating_per_score = rating_counts_df['Average_Rating']*rating_counts_df['Count']
    total_rating_score = total_rating_per_score.sum()
    
    average_rating_for_all_routes = total_rating_score/sum_of_rating_counts
    print('Average rating for all routes', round(average_rating_for_all_routes),2)
    
    climbing_type_counts = df['Climbing_Type'].value_counts()
    climbing_type_df = climbing_type_counts.reset_index()
    climbing_type_df.columns = ['Climbing_Type', 'Count']
    
    total_count_climbing_type = climbing_type_df['Count'].sum()
    
    climbing_type_df['Percentage_of_Counts'] = round(((climbing_type_df['Count'] / total_count_climbing_type) * 100),2)
    print(climbing_type_df)
    
    rock_type_counts = df['Rock_Type'].value_counts()
    rock_type_df = rock_type_counts.reset_index()
    rock_type_df.columns = ['Rock_Type', 'Count']
    
    total_count_rock_type = rock_type_df['Count'].sum()
    
    rock_type_df['Percentage_of_Counts'] = round(((rock_type_df['Count'] / total_count_rock_type) * 100),2)
    print(rock_type_df)

    return rating_counts_df, climbing_type_df, rock_type_df, average_rating_for_all_routes



def general_climbing_stats_states_and_regions(df):
    
    # Top 30 Rows for Filtering
    top_30_rows = df['Region_Route_Count'].nlargest(30)
    # Filter the DataFrame based on the top 30 values
    filtered_df = df[df['Region_Route_Count'].isin(top_30_rows)]
    print(filtered_df)
  
    return filtered_df

# =============================================================================
# Visualizations
# =============================================================================
    
# Graph for Top 30 absolute amounts of routes at a region level
def general_climbing_visuals(graph_type, df, x_variable, y_variable, grouping):
    
    fig = plt.figure(figsize=(10,6))

    top_30_values = df[y_variable].nlargest(30)
    # Filter the DataFrame based on the top 30 values
    filtered_df = df[df[y_variable].isin(top_30_values)]
    
    # Create bar plot
    graph_type(x=x_variable, y=y_variable, data=filtered_df, hue=grouping)

    # Add labels and title
    plt.xlabel('Regions')
    plt.ylabel('Route Count')
    plt.title('Route Count by Region')
    plt.xticks(rotation=90)

    fig.tight_layout()
        
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_barplot_region_abundance')
    
    return 

#%% Create visuals and output stats

# Output Stats
general_climbing_stats_states_and_regions(states_and_regions_df)
rating_counts_df, climbing_type_df, rock_type_df, average_rating_for_all_routes = general_climbing_stats_routes(routes_df)


# Output Visuals
general_climbing_visuals(sns.barplot, states_and_regions_df, 'Region', 'Region_Route_Count', 'Country_Name')

#%% Enjoyment of Routes

# =============================================================================
# What does sentiment tell us about where enthusiasim is around climbing in the world? Done
# ----> climbing_areas_df and/or climbing_sections_df
# What are the best reviewed states/regions in the world? Done
# ----> routes_df
# =============================================================================

def route_enjoyment_stats(df):
    
    remove_zero_reviews_df = df[df['Rating'] > 0]

    best_reviewed_regions_df = remove_zero_reviews_df.groupby(['Country_Name', 'State','Region']).agg({'Rating': ['mean', 'count']})
    best_reviewed_regions_df = best_reviewed_regions_df.sort_values(by=('Rating', 'mean'), ascending=False)

    print(best_reviewed_regions_df)
    
    return best_reviewed_regions_df

def route_enjoyment_visuals(df, graph_type, x_variable, y_variable, grouping, style_of_markers, size_of_markers):
    
    # Created a Figure object
    fig = plt.figure(figsize=(10,6))

    # Use Seaborn library to put markers on scatterplot
    graph_type(data=df, x=x_variable, y=y_variable, hue=grouping, style=style_of_markers, s=size_of_markers)

    # Added labels and title
    plt.xlabel('Positive Sentiment')
    plt.ylabel('Aggregate Scores')
    plt.title('Positive and Total Sentiment Across Countries')
    plt.grid(True)

    fig.tight_layout()

    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_sentiment')
    
    return

#%%

# Route Enjoyment Statistics
best_review_regions_df = route_enjoyment_stats(routes_df)

# Route Enjoyment Visuals
route_enjoyment_visuals(climbing_sections_df, sns.scatterplot, 'pos', 'compound', 'Continent_Name', 'Continent_Name', 100)


#%% Difficulty and Rock Climbing

# =============================================================================
# What is the distribution of route difficulty by country? [routes_df] 
# Does the type of rock have a relationship with the difficulty of a route? [routes_df] Done
# Does difficulty have an impact on review? [routes_df] Done
# =============================================================================

def difficult_aspects_of_climbing_visuals(df, graph_type_1, graph_type_2):
    
    remove_empty_difficulty_level_df = df[df['Difficulty_Level'].notna()]
    remove_empty_rating_df = df[df['Rating'] > 0]
    
    fig = plt.figure(figsize=(10,6))
    
    graph_type_1(x='Country_Name', hue='Difficulty_Level', data=remove_empty_difficulty_level_df, palette='viridis')

    # Add labels and title
    plt.xlabel('Country_Name')
    plt.ylabel('Difficulty Level')
    plt.title('Count Plot Difficulty by Country')
    plt.xticks(rotation=90)

    fig.tight_layout()

    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_country_difficulty')
    
        
    fig = plt.figure(figsize=(10,6))
    
    graph_type_1(x='Rock_Type', hue='Difficulty_Level', data=remove_empty_difficulty_level_df, palette='viridis')

    # Add labels and title
    plt.xlabel('Rock_Type')
    plt.ylabel('Difficulty Level')
    plt.title('Count Plot Rock Type vs Difficulty')
    plt.xticks(rotation=90)

    fig.tight_layout()

    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_rock_difficulty')
    
    fig = plt.figure(figsize=(10,6))
    
    graph_type_2(x='Difficulty_Level', y='Rating', data=remove_empty_rating_df)

    # Add title and labels
    plt.title('Violin Plot of Difficulty Level and Rating')
    plt.xlabel('Difficulty_Level')
    plt.ylabel('Rating')
    
    fig.tight_layout()

    # Saving the figure to the current directory
    fig.savefig(f'{last_name.upper()}_{first_name.upper()}_plot_difficulty_rating')
    
    return 


#%% Creating Visuals For Difficulty Understanding

difficult_aspects_of_climbing_visuals(routes_df, sns.countplot, sns.violinplot)

#%% Exporting dataframes to worksheets

# Create a Pandas Excel writer using xlsxwriter as the engine
with pd.ExcelWriter('Analyze_output.xlsx', engine='xlsxwriter') as writer:
    # Write each DataFrame to a separate sheet
    climbing_type_df.to_excel(writer, sheet_name='Climbing_Type_Reviews')
    rock_type_df.to_excel(writer, sheet_name='Rock_Type_Reviews')
    rating_counts_df.to_excel(writer, sheet_name='Distribution_of_Reviews')
    best_review_regions_df.to_excel(writer, sheet_name='Best_Reviewed_Regions')



