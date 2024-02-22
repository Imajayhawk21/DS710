#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 13:03:51 2024

@author: rajeshgogineni
"""

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
#This is the prime function that establishes if a number is a prime number or not
#0 and 1 are not considered prime numbers

def is_prime(n):
    
    #This line of code handles that n must be an integer
    if not isinstance(n, int):
        raise TypeError("Input value must be an integer")
        return
    
    #This is checking if the input value for n is negative or 0
    if n <= 0:
        raise ValueError("Input value must be non-negative")
        return
    
    #1 is not considered a prime number 
    if n == 1:
        return False

    #Check for factors from 2 to n divided by 2 plus 1 and rounded up because we want
    #it to be an integer
    for i in range(2, int(n/2) + 1):
        if n % i == 0:
            return False

    return True

#%%

def valuation(n,d):
    zz=0
    
    while n%d == 0:
        n/=d
        zz+=1
    return(zz)

#%%
#Smaller test to isolate

valuation(8,2)


#%%
#Tests to check for function validity

assert valuation(8,2) == 3
assert valuation(8,3) == 0
assert valuation(8,4) == 1
assert valuation(50,2) == 1
assert valuation(50,5) == 2
assert valuation(50,3) == 0
assert valuation(n=50,d=3) == 0
assert valuation(d=2,n=64*3) == 6


#%%

#Because we are trying to calculate separate powers for both x=3 and y=5 as divisors, 
#we need to create two different power calculations that we can then concatentate results
#to fizz or buzz respectively
def fizzbuzz_adv(n, x=3, y=5):
    
    #This line of code handles if n, x or y is 0 or if the values are not integers
    if not isinstance(n, int) or not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Input value must be an integer")
    
    if n <= 0 and isinstance(n, int):
        raise ValueError("Input value must be non-negative") 
        
    if x <= 0 and isinstance(x, int):
        raise ValueError("Input value must be non-negative") 
        
    if y <= 0 and isinstance(y, int):
        raise ValueError("Input value must be non-negative") 
    
    #We call the valuation function to get the powers for x and y 
    x_power = valuation(n, d=x)
    y_power = valuation(n, d=y)

    #concatenate powers to fizz and buzz based off results
    if n%x == 0 and n%y == 0:
        results = 'fizz' + str(x_power) + 'buzz' + str(y_power)
    elif n%x == 0:
        results = 'fizz' + str(x_power)
    elif n%y == 0:
        results = 'buzz' + str(y_power)
    else:
        results = ''
        
    return(results)

#%%

assert fizzbuzz_adv(3) == "fizz1"
assert fizzbuzz_adv(25) == "buzz2"
assert fizzbuzz_adv(75) == "fizz1buzz2"
assert fizzbuzz_adv(1) == ""
assert fizzbuzz_adv(17) == ""

#%%

#The checker should return name if it already includes the correct suffix, or name + ext if name does not include the correct suffix, adding the dot if necessary.

#user inputs the file name and the function should check if it has a dot and an extension to it
#if it already has a dot an extension of csv, txt, or python then it should just return the filename 
#if it does not have the extension then it should add it and then return the filename

#this function also needs to match the extension so if .py is the requested extension
#but the file is a .csv then we just need to add .py and return the filename with that
    
def add_filename_extension(name, ext):
    # Check if the name already ends with the provided extension including the period
    if name.endswith('.' + ext):
        return name  
        # Name already has the extension, return as is
        
    else:
        # Check if the provided extension includes a period
        if '.' in ext:
            # Split the extension into parts
            parts = ext.split('.')
            # Append the last part to the name
            return f"{name}.{parts[-1]}"
        else:
            # Append the extension to the name and return
            return f"{name}.{ext}"

#%%
#Using to work through the test cases by examining the output console 

add_filename_extension('my_csv','csv')

#%%

assert add_filename_extension('my_csv','csv') == 'my_csv.csv' #1
assert add_filename_extension('my_csv','.csv') == 'my_csv.csv' #2
assert add_filename_extension('my_csv.csv','csv') == 'my_csv.csv' #3 
assert add_filename_extension('my_csv.csv','py') == 'my_csv.csv.py' #4
assert add_filename_extension('my_csv.csv','.py') == 'my_csv.csv.py' #5

#%%
#Use your function from Subtask 2.1 and the process of currying to create two lambdas 
#add_csv(name) and add_txt(name). The output of each lambda should be a string.

#Created two new lambda functions for both csv and txt respectively

add_csv = lambda name: name if name.endswith('.csv') else name +'.csv'

add_txt = lambda name: name if name.endswith('.txt') else name +'.txt'		

#%%
#Curried function that includes the lambda functions within it

add_filename_extension = lambda name, ext: name if name.endswith(ext) and '.' in name else name + '.' + ext if '.' not in ext else name + '.' + ext.split('.')[-1]


#%%

assert add_csv('foo') == 'foo.csv'
assert add_txt('foo.bar') == 'foo.bar.txt'
assert add_txt('foo') == 'foo.txt'
assert add_txt('foo.txt.txt') == 'foo.txt.txt'

#%%
#Created a function to calculate interest, so that I could just call this within amortization.
#I noticed this repetitive nature, so it seemed to be a natural function

def interest_calc(annual_rate,principal):
    interest = ((annual_rate/12)*principal)
    return interest

#%%
#formatting for a csv file, and this will be the default

def format_csv(a,b,c,d):
    if a == "Month":
      return f"{a},{b},{c},{d}\n"
    else:
      return f"{a},{round(b,2)},{round(c,2)},{round(d,2)}\n"
  
#%%
#formatting for a tsv file 

def format_tsv(a,b,c,d):
    if a == "Month":
      return f"{a}\t{b}\t{c}\t{d}\n"
    else:
      return f"{a}\t{round(b,2)}\t{round(c,2)}\t{round(d,2)}\n"

#%%
#formatting to align items appropriately

def format_aligned(a,b,c,d):
    if a == "Month":
      return f"{a:>7}{b:>13}{c:>13}{d:>13}\n"
    else:
      return f"{a:>7}{round(b,2):13.2f}{round(c,2):>13.2f}{round(d,2):>13.2f}\n"

#%%
#This function will check is we are receiving valid numeric values so amortization calculation can proceed

def invalid_value(ii):
    if isinstance(ii, (float, int))== False or ii < 0:
        raise ValueError('An argument value must be a positive, numeric value. Please try again.')
        return None,None

#%%
#This function will check if we are receiving a string for the filename or not

def invalid_type(jj):
    if isinstance(jj, str) == False and jj is not None:
        raise TypeError('An argument should be a string. Please try again.')
        return None,None 


#%%

import pandas as pd

def amortization(principal, monthly_payment, annual_rate, filename=None, format_function=format_csv):
    Mon = 0
    # Initialize output variables

    # Check for invalid numeric values
    invalid_value(principal)  # checks validity of principal
    invalid_value(monthly_payment)  # checks validity of monthly_payment
    invalid_value(annual_rate)  # check validity of annual_rate

    # Check for invalid numeric values
    invalid_type(filename)  # check validity of filename

    # Interest is greater than monthly payment
    if interest_calc(annual_rate, principal) > monthly_payment:
        raise ValueError("Interest cannot be greater than monthly payment")
        return None, None
        # return None, None to handle certain test cases

    ###df = pd.DataFrame(columns=['Month', 'Interest', 'Balance', 'Paid_Amount'])

    # Initialize delimiter based on format function
    delimiter = ',' if format_function == format_csv else '\t'
    
    # Initialize list to store data rows
    data_rows = []

    if isinstance(filename, str) and filename:
        filename = add_txt(filename)

        with open(filename, 'w') as file:
            # Create header for file using the format function
            file.write(format_function('Month', 'Interest', 'Balance', 'Paid_Amount'))

    while principal > 0:
        Mon += 1
        interest = interest_calc(annual_rate, principal)

        # Balance + Interest - Monthly Payment
        if principal > monthly_payment or principal == monthly_payment:
            payment = monthly_payment
            principal = (principal + interest - monthly_payment)

        # Balance is less then monthly payment then you only account for interest
        elif principal < monthly_payment:
            payment = interest + principal
            principal = 0

        # This creates a dictionary with the column headers for the dataframe and appends several 
        # list of dictionaries.
        data_rows.append({
            'Month': Mon,
            'Interest': interest,
            'Balance': principal,
            'Paid_Amount': payment
        })

    # Create DataFrame from list of dictionaries
    df = pd.DataFrame(data_rows)

    # Write dataframe to file
    df.to_csv(filename, mode='a', header=False, index=False, sep=delimiter)

    Total_months = len(df)
    Total_paid = df['Paid_Amount'].sum()

    return Total_months, Total_paid