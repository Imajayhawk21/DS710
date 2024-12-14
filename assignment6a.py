#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 07:31:46 2024

@author: rajeshgogineni
"""

#%%

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
# Import necessary libraries for usage

import pandas as pd

#%%
# Task 1.1
# Reading in csv file and confirming that 1319 rows exist and 10 columns 

salary_df = pd.read_excel('2021_Salary Statistics by Employee.xlsx')
salary_df.shape

#%%
# Task 1.2 
# Global descriptive statistics variables for later usage

longest_years = salary_df['Years in Job'].max()

# Retrieve index for max Years in Job then pull name from that row
longest_years_name = salary_df.loc[salary_df['Years in Job'].idxmax(), 'Name']

longest_years_department = salary_df.loc[salary_df['Years in Job'].idxmax(), 'Sub Department']

# Used Method Chaining to extract this value 
longest_years_department_highest_salary = salary_df[salary_df['Sub Department'] == 'GEOGRAPHY & ANTHROPOLOGY']['Annual Salary'].max()


#%%
# Tests for global variables out of 1.2

assert longest_years == 45.5041095890411
assert longest_years_name == 'PLOMEDAHL, YVONNE M'
assert longest_years_department == 'GEOGRAPHY & ANTHROPOLOGY'
assert longest_years_department_highest_salary == 82468.0

#%%
# Task 1.3.1
# Created three statements that allow me to filter each component

def title_highest_paid(df, deptname):
    
    # Filter for department name    
    dept_df = df.loc[df['Sub Department'] == deptname]
    
    # Find the index of the max value
    max_salary_index = dept_df['Annual Salary'].idxmax()
    
    # Pull the working title of the highest salary 
    title_highest_paid_in_dept = dept_df.loc[max_salary_index, 'Working Title']
    
    # Return working title
    return title_highest_paid_in_dept

#%%
# Testing on specific individuals items

title_highest_paid(salary_df, 'MATHEMATICS') 

#%%
# Test function title_highest_paid function out of 1.3.1

assert title_highest_paid(salary_df, 'MATHEMATICS') == 'PROFESSOR'
assert title_highest_paid(salary_df.iloc[0:3], 'ACADEMIC AFFAIRS') == 'DIR MGMT, ANALYTICS, REPORTING'
assert title_highest_paid(salary_df.iloc[100:105], 'ALUMNI RELATIONS') == 'ATHLETICS/CORP DEVELOP SPEC'

#%%
# Task 1.3.2
# Who is in a specific salary range

def num_ppl_within_pay(df, target_pay, pay_range):
    
    # Create upper and lower bounds for this     
    lower_limit = target_pay - pay_range
    upper_limit = target_pay + pay_range
    
    # Find salaries that are within that upper and lower bound
    range_df = df[(df['Annual Salary'] >= lower_limit) & (df['Annual Salary'] <= upper_limit)]
    
    # Obtain length of dataframe after filtering to get to count
    count_of_range = len(range_df['Name'])
    
    # Return count
    return count_of_range

#%%
# For Troubleshooting

num_ppl_within_pay(salary_df, 42000, 1000)

#%%
# Tests for num_ppl_within_pay function

assert num_ppl_within_pay(salary_df, 42000, 1000) == 43
assert num_ppl_within_pay(salary_df, 100000, 10000) == 74
assert num_ppl_within_pay(salary_df, 300000, 50000) == 1 # guess who?
assert num_ppl_within_pay(salary_df[salary_df['Sub Department']=='MUSIC AND THEATRE ARTS'], 100000, 10000) == 1

#%%
# Task 1.3.3
# Count of sub department 

def largest_department(df):
    
    # Counts for each sub department
    dept_counts = df['Sub Department'].value_counts()
    
    # Get minimum value    
    max_count = dept_counts.max()
    
    # Grab index for each row that contained the minimum 
    max_value_dept = dept_counts[dept_counts == max_count].index

    return max_value_dept

#%%
# Troubleshooting largest_department function

largest_department(salary_df)


#%% 
# Tests for largest_department function 

assert largest_department(salary_df) == 'INTERCOLLEGIATE ATHLETICS'
assert largest_department(salary_df.iloc[0:300]) == 'ADVISING, RETEN & CAREER CNTR'

#%%
# Task 1.3.4
# Sub departments with the smallest amounts

def smallest_department(df):
    
    # Counts for each sub department
    dept_counts = df['Sub Department'].value_counts()
    
    # Get minimum value    
    min_count = dept_counts.min()
    
    # Grab index for each row that contained the minimum 
    smallest_depts = dept_counts[dept_counts == min_count].index
        
    # Convert to Series on output       
    return pd.Series(smallest_depts)


#%%
# Confirmation that smallest_department function is working

smallest_department(salary_df)

smallest_department(salary_df.iloc[1000:]) 

assert (smallest_department(salary_df) == pd.Series(['CAMPS & CONFERENCES', 'BARRON\\PSYCHOLOGY', 'UNIVERSITY SENATE', 'GOVERNMENTAL & COMMUN RELATION', 'STRATEGIC PLANNING', 'GRAD STUDIES/ACADEMIC AFFAIRS', 'BLUGOLD CARD OFFICE', 'BARRON\\HISTORY', 'BARRON COUNTY-ACADEMIC', 'SERVICE CENTER AND TICKETING', 'BARRON\\POLITICAL SCIENCE', 'BARRON\\KINESIOLOGY', 'BARRON\\PHYSICS', 'BARRON\\ACADEMIC SUPPORT', 'BARRON\\ART & DESIGN', 'BARRON\\BUILDING MAINTENANCE', 'BARRON\\CHEMISTRY & BIOCHEMSTRY', 'PARKING & TRANSPORTATION', 'LATIN AMER & LATINX STUDIES', 'BARRON\\COMM & JOURN', 'BARRON\\CONTINUING ED', 'LIBERAL STUDIES', 'BARRON\\FOUNDATION'])).all()
assert (smallest_department(salary_df.iloc[1000:]) == pd.Series(['SERVICE CENTER AND TICKETING', 'STRATEGIC PLANNING', 'PARKING & TRANSPORTATION', 'UNIVERSITY SENATE'])).all()

#%%
# Task 1.3.5
# Pay ratio highest against lowest 

def max_pay_ratio(df):
    
    # Calculate max annual salary and divide by minimum salary
    pay_ratio = df['Annual Salary'].max()/df['Annual Salary'].min()
    
    return pay_ratio

#%%
# Test for confirmation of max_pay_ratio function

assert max_pay_ratio(salary_df) == 9.746381540781993
assert max_pay_ratio(salary_df.iloc[1000:]) == 5.145001117603857

#%%

#%%
# Task 2.1
# Reading in full csv file

housing_master_df = pd.read_csv('HPI_master.csv')
housing_master_df.shape

housing_master_df.head
housing_master_df.tail

# Used for troubleshooting when I was not passing pytests (named the variable wrong)
type(housing_master_df)

#%%
# Task 2.2
# Filtered housing_master_df and confirming that 60000+ rows exist 

# =============================================================================
# Housing_df, 
# 
# containing only the records in the set for which the "level" is "MSA"
# 
# "hpi_flavor" is "all-transactions".
# =============================================================================

housing_df = housing_master_df[(housing_master_df['level'] == 'MSA') & (housing_master_df['hpi_flavor'] == 'all-transactions')]
housing_df.shape
housing_df.head()


#%%
# Task 2.3.1

# =============================================================================
# place_with_highest_price(df, time), 
# 
# where time is a tuple of order two as (year, period)	
# =============================================================================

def place_with_highest_price(df, time):
    
    # Separate the tuple into two variables
    year, period = time
    
    # Filter by year and period    
    filtered_df = df[(df['yr'] == year) & (df['period'] == period)]
    
    # Retrieve max value index in index_nsa column 
    max_index_nsa = filtered_df['index_nsa'].idxmax()
    
    # Output place_name of highest cost
    max_value_place_name = df.loc[max_index_nsa, 'place_name']

    return max_value_place_name

#%%
# Used for isolated testing 

place_with_highest_price(housing_df, (2022,1) ) 

#%%
# Test to confirm place_with_highest_price function is working correctly

place_with_highest_price(housing_df, (2022,1) ) == 'Austin-Round Rock-Georgetown, TX'


#%%
# Task 2.3.2

# =============================================================================
# 
# For a given placename (string), in what (year,period) 
#
# did the price index first go above a given price (float)?
# 
# =============================================================================

def time_price_first_above(df, place, price):
    
    # Filter by year and period    
    filtered_df = df[(df['place_name'] == place) & (df['index_nsa'] >= price)]
    
    # Extract year for relevant row
    row_year = filtered_df.loc[filtered_df.index[0], 'yr']
    
    # Extract period for relevant row
    row_period = filtered_df.loc[filtered_df.index[0], 'period']
    
    # Create tuple
    row_year_period = (row_year,row_period)
    
    return row_year_period # return tuple values
    
    # Filter by year and period    
    matching_df = df[(df['place_name'] == place) & (df['period'] >= price)]
    
    row = matching_df.loc[matching_df.index[0]]
    
    year = df.loc[row, 'year']

    return tuple(year,period)

#%%
# Tests to confirm time_price_first_above function 

time_price_first_above(housing_df,'Orlando-Kissimmee-Sanford, FL', 200) == (2005,2)
time_price_first_above(housing_df,'Eau Claire, WI', 200) == (2016, 2)

#%%
# Task 2.3.3

# =============================================================================
# 
# For a given placename (string) and a pair of years & periods (two pairs of integers) 
#
# what was the price change ratio?
#
# =============================================================================

def price_ratio(df, place, t1, t2):
    
    # Creating the range of values to look for 
    filtered_t1_df = df[(df['place_name'] == place) & (df['yr'] == t1[0]) & (df['period'] == t1[1])] 
    filtered_t2_df = df[(df['place_name'] == place) & (df['yr'] == t2[0]) & (df['period'] == t2[1])]    
    
    # Extract high and low price for place_name
    t1_price = filtered_t1_df.loc[filtered_t1_df.index[0], 'index_nsa']       
    t2_price = filtered_t2_df.loc[filtered_t2_df.index[0], 'index_nsa']
    
    # Calculate price ratio
    comp_price_ratio = t2_price/t1_price
    
    return comp_price_ratio

#%%
# Tests to confirm function price ratio is working as expected

price_ratio(housing_df,'Kokomo, IN',(1999,1),(2000,3)) == 1.045124439004488
price_ratio(housing_df,'Eau Claire, WI',(2000,1),(2020,1)) == 1.8048886948930596


