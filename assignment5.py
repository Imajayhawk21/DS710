#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 12:22:35 2024

@author: rajeshgogineni
"""
#%%

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
# Necessary libraries to execute work

import numpy as np

import matplotlib.pyplot as plt


#%%
# Check if zeros are present in an array or not

def has_zeros(arr):
    
    if 0 in arr:
        return True
        
    else:
        return False


#%%
# Tests to check if has_zeros has 0's or not in it

assert has_zeros(np.array([0,0,0,1,1,1,13,3,3,3])) == True
assert has_zeros(np.array([[0,0,0],[1,1,1],[13,3,3]])) == True
assert has_zeros(np.array([1,1,1,13,3,3,3])) == False
assert has_zeros(np.array([[1,1,1],[13,3,3]])) == False

assert has_zeros(np.array([0.000001, -0.000001])) == False
assert has_zeros(np.array([[1,2,3,4],[1e-1, 1e-2, 1e-3, 1e-4]])) == False

#%%
# Tolerance check if any value in array is close enough to zero

def has_approximate_zeros(arr, tol):
  
# =============================================================================
#   arr - is the array that is being passed into the function
#
#   tol - if the tolerance that is evaluated for each value in the array 
#   to check if the value is close enough to zero  
#   
#   np.abs - is taking all numbers and setting them to their absolute value 
#
#   < tol - is checking if that absolute value is less than the tolerance level
#
#   .any - is evaluating if any value in the array meets that criteria 
# =============================================================================
    
    return (np.abs(arr) < tol).any()


    
#%%
# Tests to check if has_approximate works the way intended

assert has_approximate_zeros(np.array([0,0,1e-10,1,1,1,13,3,3,3]), 1e-7) == True
assert has_approximate_zeros(np.array([[0,1e-10,1e-5],[1,1,1],[13,3,3]]), 1e-7) == True
assert has_approximate_zeros(np.array([-1e-8,1,1,13,3,3,3]), 1e-7) == True
assert has_approximate_zeros(np.array([[-2e-9,1,1],[13,3,3]]), 1e-9) == False

assert has_approximate_zeros(np.array([0.000001, -0.000001]), 1e-10) == False
assert has_approximate_zeros(np.array([[1,2,3,4],[1e-1, 1e-2, 1e-3, 1e-4]]), 1e-10) == False

#%%
# This is the prime function that establishes if a number is a prime number or not
# 0 and 1 are not considered prime numbers

def is_prime(n):
    
    # This line of code handles that n must be an integer
    if not isinstance(n, int):
        raise TypeError("Input value must be an integer")
        return
    
    # This is checking if the input value for n is negative or 0
    if n <= 0:
        raise ValueError("Input value must be positive")
        return
    
    # 1 is not considered a prime number 
    if n == 1:
        return False

    # Check for factors from 2 to n divided by 2 plus 1 and rounded up because we want
    # it to be an integer
    for i in range(2, int(n/2) + 1):
        if n % i == 0:
            return False

    return True

#%%

def primes(lower, upper):

# =============================================================================
#   lower - your lower bound number that will be evaluated by primes()
#
#   upper - your upper bound -1 that will be evaluated by primes()
#
#   the return will return each number passed into a list
# =============================================================================

    return [n for n in range(lower, upper) if is_prime(n)]
    

#%%
# Within the assert statements the lists are converted into arrays with np.array
# Test cases to check if primes() is working correctly

assert np.all(primes(2,7) == np.array([2,3,5])) 
assert np.all(primes(2,8) == np.array([2,3,5,7]))
assert np.all(primes(2,9) == np.array([2,3,5,7]))

#%%
# Output array that contain average, max, minimum and count of zeros 

def column_statistics(arr):
    
    # Statistical tests being conducted 
    column_means = np.mean(arr, axis=0)
    column_max = np.max(arr, axis=0)
    column_min = np.min(arr, axis=0)
    count_zeros = np.count_nonzero(arr == 0, axis=0)


    return np.array([column_means, column_min, column_max, count_zeros])
    
#%%
# Test I was using for verification for column_statistics()

column_statistics(np.array([ [1,0,3], [4,5,-1] ]))


#%%
#For the sake of testing, so that I can verify if the task 3 function is 
#working as desired

# =============================================================================
# arr = np.array([ [1,0,3],
#                  [4,5,-1]
#                ])
# # arr has three columns, so output will have three columns
# 
# 
# column_statistics(arr) ==
#     np.array([
#           [2.5,2.5,1],   # means of each column
#           [1,0,-1],      # min of each column
#           [4,5,3],       # max of each column
#           [0,1,0]        # number of zero entries
#         ])
# 
# =============================================================================

#%%
# I created a function that allowed us to take filename and any amount of 
# requested rows

# def count_strings_in_csv(filename, n=None):
    
#     # Read the CSV file into a NumPy array
#     data = np.genfromtxt(filename, delimiter=',', dtype=str)
    
#     print(data[0])
    
#     # Flatten the array to a 1D array
#     flattened_data = data.flatten()
    
#     print(flattened_data)

#     # Count the occurrences of each string
#     unique_strings, counts = np.unique(flattened_data, return_counts=True)

#     # ****Troubleshooting code****
#     #Something is going wrong here
    
#     print("First few rows of unique_strings:")
#     print(unique_strings[:5])  # Adjust the slice as needed to display more or fewer rows
    
#     print("First few rows of counts:")
#     print(counts[:5])  # Adjust the slice as needed to display more or fewer rows
    
#     # Create a dictionary from the unique strings and counts
#     count_of_words = dict(zip(unique_strings, counts))
    
#     # Sort the dictionary based on values in descending order
#     sorted_word_frequency = sorted(count_of_words.items(), key=lambda x: x[1], reverse=True)
        
#     if n is None:
#         n = len(sorted_word_frequency)
    
#     # Take the top n entries
#     top_n = dict(sorted_word_frequency[:n])
        
#     return top_n

#%%
# Function for troubleshooting

def count_strings_in_csv(filename, n=None):
    
    # Read the CSV file into a NumPy array
    data = np.genfromtxt(filename, delimiter=',', dtype=str)
    
    # Convert array to dictionary using dictionary comprehension
    word_frequency = {item[0]: int(item[1]) for item in data}

    return word_frequency

#%%

# Replace 'filename.csv' with the path to your CSV file
filename = 'word_frequencies_alice.csv'
word_frequency = count_strings_in_csv(filename)

#%%

frequencies_unsorted = np.array(list(word_frequency.values()))

#%%

frequencies_sorted = np.sort(frequencies_unsorted)[::-1]

#%%

frequency_of_word = frequencies_sorted[0:20]

#%%

def plot_word_frequencies(filename, n=None):
    
    # Create a Figure object
    fig = plt.figure()
        
    top_n = count_strings_in_csv(filename, n)
    
    # Sort the dictionary keys based on their corresponding values
    sorted_keys = sorted(top_n, key=top_n.get, reverse=True)
    top_n_values = [top_n[key] for key in sorted_keys]
    
    # Create a list of ranks from 1 to the number of words
    ranks = list(range(1, len(top_n) + 1))
    
    plt.bar(ranks, top_n_values)
    plt.xlabel('Rank')
    plt.ylabel('Frequency of Words')
    plt.title(f'Top {len(top_n)} Words Frequency')
    plt.xticks(ranks, ranks, rotation=45, ha='right')  # Set x-ticks as sorted keys
    
    # Add the word values on top of or inside the bars
    for i, (key, value) in enumerate(zip(sorted_keys, top_n_values)):
        plt.text(i + 1, value, key, ha='center', va='bottom')  # Place word label on top of the bar
    
    fig.tight_layout()
    
    
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign5_task4.png')
        
    return 
#%%

plot_word_frequencies(filename, 20)

#%%
#100 spaces from 0 to 1

x = np.array(np.linspace(0, 1, num=100))

#%%

function_values = np.zeros((5, 100))

#%%
#Convert equations to python code

# =============================================================================
# Row 0 : 2 * (x - 1/2)
#
# Row 1 : (3**2 / 2) * (x - 1/3) * (x - 2/3)
#
# Row 2 : (4**3 / (2 * 3)) * (x - 1/4) * (x - 2/4) * (x - 3/4)
#
# Row 3 : (5**4 / (2 * 3 * 4)) * (x - 1/5) * (x - 2/5) * (x - 3/5) * (x - 4/5)
#
# Row 4 : (6**5 / (2 * 3 * 4 * 5)) * (x - 1/6) * (x - 2/6) * (x - 3/6) * (x - 4/6) * (x - 5/6)
# =============================================================================

#%%
#create functions and insert into each respective list

# Define your five functions
def f_1(x):
    return 2*(x-1/2)

def f_2(x):
    return (3**2 / 2) * (x - 1/3) * (x - 2/3)

def f_3(x):
    return (4**3 / (2 * 3)) * (x - 1/4) * (x - 2/4) * (x - 3/4)

def f_4(x):
    return (5**4 / (2 * 3 * 4)) * (x - 1/5) * (x - 2/5) * (x - 3/5) * (x - 4/5)

def f_5(x):
    return (6**5 / (2 * 3 * 4 * 5)) * (x - 1/6) * (x - 2/6) * (x - 3/6) * (x - 4/6) * (x - 5/6)

#%%
# Combine the results into a 5-row array, by putting respective function 
# into respective row

function_values[0] = f_1(x)
function_values[1] = f_2(x)
function_values[2] = f_3(x)
function_values[3] = f_4(x)
function_values[4] = f_5(x)

#%%
# I considered using a function here, but choose not because I did 
# not see where this could be reused

# Createed a Figure object
fig = plt.figure()

# Plotted each row as a line
for i in range(function_values.shape[0]):
    plt.plot(function_values[i], label=f'f_{i+1}')

# Added labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of Each Function')
plt.legend()
plt.grid(True)

# Set x-axis limits and ticks
plt.xlim(0, 100)
plt.xticks(np.linspace(0, 100, num=5), np.linspace(0, 1, num=5))  # Adjust ticks and labels


# Show the plot
fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign5_task5.png')


#%%    
# Taking the mean of the wait times supplied by the random generated array

def mean_wait(bus_times):
    
    mean_wait_time = np.mean(bus_times)
    
    return mean_wait_time

#%%    
# The shortest wait time supplied by the random generated array

def shortest_wait(bus_times):
    
    shortest_wait_time = np.min(bus_times)
    
    return shortest_wait_time    

#%%    
# The longest wait time supplied by the random generated array

def longest_wait(bus_times):
    
    longest_wait_time = np.max(bus_times)
    
    return longest_wait_time      

#%%
# Time from midnight cumulative sum

def cumulative_wait(bus_times):
    
    cum_bus_waits = np.cumsum(bus_times)
    
    return cum_bus_waits

#%%
# Random generation of a bus wait time using the amount of busses and the mean wait time

def simulate_busses(mean, num_busses):
      
    bus_times = np.round(np.random.exponential(scale=mean, size=num_busses),2)   
    
    mean_wait_time = mean_wait(bus_times)
    shortest_wait_time  = shortest_wait(bus_times)
    longest_wait_time = longest_wait(bus_times)
    cum_bus_waits = cumulative_wait(bus_times)
    
    return np.array(bus_times), [mean_wait_time,shortest_wait_time,longest_wait_time], [cum_bus_waits]

#%%

bus_times = simulate_busses(15, 50)[0]

#%%

def line_cumulative_wait_plot(mean, num_busses):
    
    # Created a Figure object
    fig = plt.figure()
        
    bus_times, stats_wait_times, [cum_bus_waits] = simulate_busses(mean, num_busses)
        
    # Created a list of ranks from 1 to the number of words
    bus_amount = list(range(1, len(cum_bus_waits) + 1))  
    
    plt.plot(bus_amount, cum_bus_waits, marker='o', linestyle='-')

    # Added labels and title
    plt.xlabel('bus number')
    plt.ylabel('arrival time (minutes)')
    plt.title('Cumulative Wait Time Over The Day')
    plt.grid(True)

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign5_task6_line.png')
            
    return                         

#%%
# Create line_cumulative_wait_plot

line_cumulative_wait_plot(15, 50)

#%%

def histogram_wait_times(mean, num_busses):
    
    # Created a Figure object
    fig = plt.figure()
        
    bus_times, stats_wait_times, [cum_bus_waits] = simulate_busses(mean, num_busses)
            
    # Plotted these in 10 bins
    plt.hist(bus_times, bins=10, color='blue', edgecolor='black')
    

    # Added labels and title
    plt.xlabel('wait time (minutes)')
    plt.ylabel('count')
    plt.title('Distribution of Wait Times')
    plt.grid(True)

    fig.tight_layout()
    
    # Saving the figure to the current directory
    fig.savefig(f'{first_name.upper()}_{last_name.upper()}_plot_assign5_task6_hist.png')
            
    return 

#%%
# Create histogram plot for wait times 

histogram_wait_times(15, 50)

