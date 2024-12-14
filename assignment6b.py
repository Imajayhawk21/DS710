#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 00:20:14 2024

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


#%%
# Task 1.1
# Reading in csv file and confirming that 1319 rows exist and 10 columns 

salary_df = pd.read_excel('2021_Salary Statistics by Employee.xlsx')
salary_df.shape

# Grab names of columsn to confirm during other activities
col_names = salary_df.columns.tolist()
print(col_names)

#%%
# Task 1.2 

def salary_tenure(df):
    
    # Created a Figure object
    fig = plt.figure()
        
    # Pull out annual salary and years in job and make them variables
    annual_salary, tenure = df['Annual Salary'], df['Years in Job']
    
    # Plot x and y variables in this order in a scatterplot
    plt.scatter(tenure, annual_salary)

    # Added labels and title
    plt.xlabel('Years in Job')
    plt.ylabel('Annual Salary')
    plt.title('Tenure as it Relates to Salary')
    plt.grid(True)

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task1-2.png')
            
    return      

#%%
# Create scatterplot and save it for task 1.2

salary_tenure(salary_df)

#%%
# Task 1.3

def salary_tenure_1_3(df):
    
    # Created a Figure object
    fig = plt.figure()
        
    # Pull out annual salary, years in job, and pay basis and make them variables
    annual_salary, tenure , pay_basis= df['Annual Salary'], df['Years in Job'], df['Pay Basis']
    
    # Use Seaborn library to put markers on scatterplot
    sns.scatterplot(data=df, x=tenure, y=annual_salary, hue=pay_basis, style=pay_basis, markers=['o', 's', 'D'])

    # Added labels and title
    plt.xlabel('Years in Job')
    plt.ylabel('Annual Salary')
    plt.title('Salary as it Relates to Tenure and Pay Type')
    plt.grid(True)

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task1-3.png')
            
    return    

#%%
# Create scatterplot and save it for task 1.3

salary_tenure_1_3(salary_df)

#%%
# Task 1.4.1

def salary_pay_basis(df):
    
    # Created a Figure object
    fig = plt.figure()
        
    # Pull out annual salary and pay basis and make them variables
    annual_salary, pay_basis= df['Annual Salary'], df['Pay Basis']
    
    # Use Seaborn library to create violin plots
    sns.violinplot(data=df, x=pay_basis, y=annual_salary, hue=pay_basis, palette='muted')


    # Added labels and title
    plt.xlabel('Pay Basis Categories')
    plt.ylabel('Annual Salary')
    plt.title('Violin Plot for Each Pay Basis')

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task1-4-1.png')
            
    return

#%%

salary_pay_basis(salary_df)

#%%
# Task 1.4.2

def salary_empl_class_code(df):
    
    # Created a Figure object
    fig = plt.figure()
        
    # Pull out annual salary and pay basis and make them variables
    annual_salary, empl_code= df['Annual Salary'], df['Empl Class Code']
    
    # Use Seaborn library to put markers on scatterplot
    sns.violinplot(data=df, x=empl_code, y=annual_salary, hue=empl_code, palette='muted')


    # Added labels and title
    plt.xlabel('Employee Class Code Categories')
    plt.ylabel('Annual Salary')
    plt.title('Violin Plot for Each Employee Code')

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task1-4-2.png')
            
    return

#%%

salary_empl_class_code(salary_df)

#%%
# Task 1.4.3

def salary_sub_dept_faculty(df):
    
    # Created a Figure object
    fig = plt.figure(figsize=(10,6))
    
    filtered_df = df[df['Empl Class Code'] == 'FA']
    
    # Pull out annual salary and pay basis and make them variables
    annual_salary, dept_fa_only = filtered_df['Annual Salary'], filtered_df['Sub Department']
        
    # Use Seaborn library to put markers on scatterplot
    sns.violinplot(data=filtered_df, x=dept_fa_only, y=annual_salary, hue=dept_fa_only, 
                   palette='muted', width=0.5, alpha=0.7)


    # Added labels and title
    plt.xlabel('Sub Department')
    plt.ylabel('Annual Salary')
    plt.title('Violin Plot for Faculty for Each Sub Department')
    
    # Rotate the x-axis labels by 90 degrees
    plt.xticks(rotation=90)
    
    # Remove the legend
    plt.legend().remove()
    
    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task1-4-3.png')
            
    return

#%%

salary_sub_dept_faculty(salary_df)

#%%
# Task 1.5

def pay_basis_hist(df):
    
    # Created a Figure object
    fig = plt.figure()
    
    # Select only the columns you need
    subset_df = df[['Pay Basis', 'Annual Salary']]
            
    # Pivot the DataFrame to get separate columns for each type of house
    pivot_df = subset_df.pivot_table(index=df.index, columns='Pay Basis', values='Annual Salary', aggfunc='first')

    # Plot the stacked histogram
    pivot_df.plot.hist(stacked=True, bins=40)

    # Add labels and title
    plt.xlabel('Pay Basis')
    plt.ylabel('Frequency')
    plt.title('Stacked Histogram of Annual Salary by Pay Basis')
    plt.legend()
    
    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task1-5.png')

#%%

pay_basis_hist(salary_df)

#%%
# Task 1.6

def salary_dept_scatter_plots(df):
    
    # Created a Figure object
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

# =============================================================================
# 
# Make a figure with two subplots / sets of axes, side-by-side.
#
# In the left subplot: A scatter of salary (y) vs years in job (x) for the "facilities custodial services" department.
# In the right subplot: A scatter of salary (y) vs years in job (x) for the "mathematics" department.
# 
# Make sure that both plots use the same axes bounds, otherwise the visual comparison is nearly meaningless.
# 
# =============================================================================

    # Filtering for dataframes to create subplots
    fcs_df = df[df['Sub Department'] == 'FACILITIES CUSTODIAL SERVICES']    
    math_df = df[df['Sub Department'] == 'MATHEMATICS']
    
    
    # Plot scatter plot for the first subplot
    sns.scatterplot(x='Years in Job', y='Annual Salary', data=fcs_df, ax=ax1)
    sns.regplot(x='Years in Job', y='Annual Salary', data=fcs_df, ax=ax1)  # Add regression line

    # Plot scatter plot for the second subplot
    sns.scatterplot(x='Years in Job', y='Annual Salary', data=math_df, ax=ax2)
    sns.regplot(x='Years in Job', y='Annual Salary', data=math_df, ax=ax2)  # Add regression line
    
    
    # Get the maximum value of a specific column in each subsetted dataframe
    max_salary_df1 = fcs_df['Annual Salary'].max()
    max_salary_df2 = math_df['Annual Salary'].max()
    
    max_tenure_df1 = fcs_df['Years in Job'].max()
    max_tenure_df2 = math_df['Years in Job'].max()
    
    ylim_max_salary = max(max_salary_df1, max_salary_df2)
    xlim_max_tenure = max(max_tenure_df1, max_tenure_df2)

    
    # Added labels and title
    ax1.set_title('Facilties Custodial Services')
    ax1.set_xlabel('Years of Service')
    ax1.set_ylabel('Annual Salary')
    
    ax2.set_title('Mathematics')
    ax2.set_xlabel('Years of Service')
    ax2.set_ylabel('Annual Salary')

    
    # Set the limits for the x and y axes 
    ax1.set_xlim(0, xlim_max_tenure)
    ax1.set_ylim(0, ylim_max_salary)
    ax2.set_xlim(0, xlim_max_tenure)
    ax2.set_ylim(0, ylim_max_salary)
    
    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task1-6.png')

    return    

#%%

salary_dept_scatter_plots(salary_df)

#%%
# Task 2.1
# Reading in full csv file

housing_master_df = pd.read_csv('HPI_master.csv')
housing_master_df.shape

housing_master_df.head
housing_master_df.tail


# Filtered housing_master_df and confirming that 60000+ rows exist 

# =============================================================================
# Housing_df
# containing only the records in the set for which the "level" is "MSA"
# "hpi_flavor" is "all-transactions".
# =============================================================================

housing_df = housing_master_df[(housing_master_df['level'] == 'MSA') & (housing_master_df['hpi_flavor'] == 'all-transactions')]
housing_df.shape
housing_df.head()
housing_df.dtypes

#%%
# Task 2.2

def plot_price_for_places(df, places):
    
# =============================================================================
# This function plots the HPI for each place on one axes. 
# On the y-axis is price, and on the x-axis is time. 
# The plot must include a legend. 
# The function returns the axis and figure objects containing the plot. 
# =============================================================================
    
    fig, ax = plt.subplots()

    # Filter to get relevant places only
    filtered_housing_df = df[df['place_name'].isin(places)]
    
    # Combine year and period into one column for the sake of graphing later
    filtered_housing_df['yr_with_period'] = filtered_housing_df['yr']+0.25*filtered_housing_df['period']
    
    # Plot the data
    sns.lineplot(x='yr_with_period', y='index_nsa', hue='place_name', data=filtered_housing_df)
    
    # Added labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Price Over Time For Different Places')
    ax.legend(title='Location')
    
    return fig, ax

#%%

fig, ax = plot_price_for_places(housing_master_df ,['Eau Claire, WI','Fort Collins, CO','South Bend-Mishawaka, IN-MI','Raleigh-Cary, NC'])

fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task2-2-ec-fc-sb-ra.png')


#%%

fig, ax = plot_price_for_places(housing_master_df ,['Eau Claire, WI', 'Madison, WI', 'Green Bay, WI'])

fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task2-2-WI.png')

#%%
# Task 2.3

def plot_price_hist(df, t1, t2):
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12,6))
    
    # Filtering for dataframes to create subplots    
    time_period_1_df = df.loc[(df['yr'] == t1[0]) & (df['period'] == t1[1])]
    time_period_2_df = df.loc[(df['yr'] == t2[0]) & (df['period'] == t2[1])]
    
    # Plot the two histograms
    sns.histplot(data=time_period_1_df, x='index_nsa', ax=ax1, bins=8)
    sns.histplot(data=time_period_2_df, x='index_nsa', ax=ax2, bins=8)   
    
    # Find the maximum count between the histograms
    max_count = max(ax1.get_ylim()[1], ax2.get_ylim()[1])
    min_count = min(ax1.get_ylim()[0], ax2.get_ylim()[0])


    # Get the maximum value of a specific column in each subsetted dataframe
    max_index_nsa_df1 = time_period_1_df['index_nsa'].max()
    max_index_nsa_df2 = time_period_2_df['index_nsa'].max()
    
    # Get the minimum value of a specific column in each subsetted dataframe
    min_index_nsa_df1 = time_period_1_df['index_nsa'].min()
    min_index_nsa_df2 = time_period_2_df['index_nsa'].min()
    
    # Get the minimum and maximum values for each subplot to size x label the same
    xlim_max_index_nsa = max(max_index_nsa_df1, max_index_nsa_df2)
    xlim_min_index_nsa = min(min_index_nsa_df1, min_index_nsa_df2)

    # Added labels and title
    ax1.set_title(f'Pricing trend for Year {t1[0]} , Period {t1[1]}')
    ax1.set_xlabel('Thousands of $')
    ax1.set_ylabel('Frequency')
    
    ax2.set_title(f'Pricing Trend for Year {t2[0]} , Period {t2[1]}')
    ax2.set_xlabel('Thousands of $')
    ax2.set_ylabel('Frequency')

    # # Set the limits for the x and y axes 
    ax1.set_xlim(xlim_min_index_nsa, xlim_max_index_nsa)
    ax1.set_ylim(min_count, max_count)
    ax2.set_xlim(xlim_min_index_nsa, xlim_max_index_nsa)
    ax2.set_ylim(min_count, max_count)
    
    fig.tight_layout()
    
    return fig, (ax1, ax2)

#%%

fig, ax = plot_price_hist(housing_df, (2010,1), (2020,1))

fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign6b_task2-3.png')

