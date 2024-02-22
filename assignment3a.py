#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 23:43:52 2024

@author: rajeshgogineni
"""

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
#This is the prime function that establishes if a number is a prime number or not

def is_prime(n):
    #0 and 1 are not considered prime numbers
    if n <= 1:
        return False

    #Check for factors from 2 to n divided by 2 plus 1 and rounded up because we want
    #it to be an integer
    for i in range(2, int(n/2) + 1):
        if n % i == 0:
            return False

    return True

#%%
#Testing this function out to make sure it works with a few numbers that I know are prime 
#and that I know are not prime

is_prime(10)

#%%
is_prime(3)

#%%
is_prime(53)


#%%
#assert statements to check if def is_prime is working as intended

assert not is_prime(0)
assert not is_prime(1)
assert is_prime(2)
assert is_prime(3)
assert not is_prime(10)

#%%
#If something is less than or equal to one then that is not considered a prime number
#We will just immediately return a 0 for our count of prime numbers

def num_primes_to(n):
    if n <= 1:
        return 0
    
    #Initialize num_primes to start the counting process as we go through the for loops
    num_primes = 0

    # Check prime numbers up to n+1
    for num in range(2, n+1):
        is_prime = True
        # We divide by 2 and add 1 to go through this for loop. We are checking for when a divisor
        #makes it so there is no remainder and we will count each prime number up to our submitted
        #n value
        for divisor in range(2, int(num/2) + 1):
            if num % divisor == 0:
                is_prime = False
                break
        else:
            num_primes += 1

    return num_primes 

#%%
#Smaller checks that I am performing as I was troubleshooting the function
#I also added print statements in the function to determine what was happening during each loop

num_primes_to(10)

#%%
#Confirm if these values are met 

assert num_primes_to(-5) == 0
assert num_primes_to(2) == 1
assert num_primes_to(3) == 2
assert num_primes_to(10) == 4

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
    if not isinstance(n, int) or n <= 0 or not isinstance(x, int) or x <= 0 or not isinstance(y, int) or y <= 0:
        return "invalid"
    
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

fizzbuzz_adv(0)


#%%

assert fizzbuzz_adv(3) == "fizz1"
assert fizzbuzz_adv(25) == "buzz2"
assert fizzbuzz_adv(75) == "fizz1buzz2"
assert fizzbuzz_adv(1) == ""
assert fizzbuzz_adv(0) == "invalid"
assert fizzbuzz_adv(3.1415) == "invalid"
assert fizzbuzz_adv(-15) == "invalid"

#%%

from datetime import datetime, timedelta

def minutes_to_midnight(time=None):
    # Current time needs to be populated if a time is not provided.
    #I identified this after a failure in pytests and addressed it after that
    if time is None:
        time = datetime.now()  
        
    # Calculates midnight time for the next day
    midnight = (time + timedelta(days=1)).replace(hour=0, minute=0, second=0)

    # Calculates the difference in minutes between current time and midnight
    difference = midnight - time
    minutes_left = difference.total_seconds() // 60

    return minutes_left

#%%

#This section allows us to test an input datetime into the function and print the output
minutes_left = minutes_to_midnight(datetime.fromisoformat('2011-11-04T00:00:00'))

print("Minutes left until midnight:", minutes_left)

#%%

assert minutes_to_midnight(datetime.fromisoformat('2011-11-04T05:23:47')) == 1440 - 324
#                                                              HH MM SS

assert minutes_to_midnight(datetime.fromisoformat('2011-11-04T23:59:00')) == 1
assert minutes_to_midnight(datetime.fromisoformat('2011-11-04T23:59:01')) == 0
assert minutes_to_midnight(datetime.fromisoformat('2011-11-04T23:59:59')) == 0

assert minutes_to_midnight(datetime.fromisoformat('2011-11-04T00:00:00')) == 1440
assert minutes_to_midnight(datetime.fromisoformat('2011-11-04T00:00:01')) == 1440-1


#%%
#Created a function to calculate interest, so that I could just call this within amortization.
#I noticed this repetitive nature, so it seemed to be a natural function

def interest_calc(annual_rate,principal):
    interest = ((annual_rate/12)*principal)
    return interest

#%%

import pandas as pd

def amortization(principal, monthly_payment, annual_rate):
    Mon = 0
    #Initialize output variables

    df = pd.DataFrame(columns=['Month', 'Interest', 'Remaining_Balance', 'Paid_Amount'])
    
    while principal > 0:
        Mon = Mon + 1
        interest = interest_calc(annual_rate, principal)
        
        #Interest is greater than monthly payment
        if interest > monthly_payment:
            print("You have to increase your current monthly payment to be able to pay off your loan")
            return None, None
        #return None, None to handle certain test cases
        
        #Balance + Interest - Monthly Payment
        elif principal > monthly_payment or principal == monthly_payment: 
            payment = monthly_payment
            principal = (principal + interest - monthly_payment) 
                         
        #Balance is less then monthly payment then you only account for interest
        elif principal < monthly_payment: 
            payment = interest + principal
            principal = 0
        
        #Dataframe that I am appending to as each row is being created
        data = pd.DataFrame([[Mon, interest, principal, payment]], columns=['Month', 'Interest', 'Remaining_Balance', 'Paid_Amount'])
        
        df = pd.concat([df, data], ignore_index=True)
        
    Total_months = len(df)
    Total_paid = df['Paid_Amount'].sum()
            
    return(Total_months, Total_paid)

#%%



#%%

test_case_months, test_case_paid = amortization(principal=500, monthly_payment=100, annual_rate=0.05)
assert test_case_months == 6
assert (test_case_paid - 506.346103) < 0.00001
assert (506.346103 - test_case_paid) < 0.00001

#%%

test_case_months, test_case_paid = amortization(500,1,0.05)
assert test_case_months is None
assert test_case_paid is None

#%%

amortization(500, 500, 0.05)
