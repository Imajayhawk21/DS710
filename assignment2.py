#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 21:35:39 2024

@author: rajeshgogineni
"""

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
#We need to compute the greatest power of a given number that divides another
#We can do this by looping over a number using a while statement
#I did not do this as a function, but probably could have changed these to a function in order
#to reduce the total amount of code written

#if creating a function I would concatenate the variables to val to create a new variable for each function

ii=0

while 24%2**ii == 0:
    ii=ii+1
    val_2_24=ii-1
        
jj=0
    
while 24%5**jj == 0:
    jj=jj+1
    val_5_24=jj-1
    
tt=0
    
while 30%3**tt == 0:
    tt=tt+1
    val_3_30=tt-1
    
zz=0
    
while 10540974080%2**zz == 0:
    zz=zz+1
    val_2_10540974080=zz-1
    
#%%
#Count how many prime numbers are between 1 and 999 excluding 0 and 1
#We know the range, so I utilized a for loop because of that. I started with 2 because
#we wanted to not include 1 and 0.

#I counted all the numbers that were not primes and those that were prime by using two nested loops

num_nonprimes=0
num_primes=0

for x in range (2,999):
    for y in range (2,x):
        if x%y==0:
            num_nonprimes=num_nonprimes+1
            break 
    else:
        num_primes=num_primes+1
            

#%%
#BAL is the Balance 
#IR is the Interest Rate
#MP is the Monthly Payment
#I is the Interest Accured in the Month
#Mon is the Month

import pandas as pd

def calculate_loan(BAL, IR, MP, Mon):

    #Initialize output variables

    df = pd.DataFrame(columns=['Month', 'Interest', 'Remaining_Balance', 'Paid_Amount'])
    
    while BAL > 0:
        Mon = Mon + 1
        I = (IR/12)*BAL
        
        if I > MP:
            print("You may have to pay more than your current monthly payment to be able to pay off the loan")
            break
        
        elif BAL > MP or BAL == MP: 
            PA = MP
            BAL = (BAL + ((IR/12)*BAL)) - MP #Balance + Interest - Monthly Payment

                
        elif BAL < MP: #Balance is less then monthly payment then you only account for interest
            PA = I + BAL
            BAL = 0
            
        data = pd.DataFrame([[Mon, I, BAL, PA]], columns=['Month', 'Interest', 'Remaining_Balance', 'Paid_Amount'])
        
        df = pd.concat([df, data], ignore_index=True)
        
    Total_months = len(df)
    Total_paid = df['Paid_Amount'].sum()
            
    return(Total_months, Total_paid)

#%%
#Calling the functions I have defined to test the different tests in 3.2
    
loan_500_pay_100_int_05 = calculate_loan(500, 0.05, 100, 0)

test_p500_r5_mp100_number_of_months, test_p500_r5_mp100_total_paid = loan_500_pay_100_int_05   

loan_500_pay_500_int_05 = calculate_loan(500, 0.05, 500, 0)

test_p500_r5_mp500_number_of_months, test_p500_r5_mp500_total_paid = loan_500_pay_500_int_05   

#%%
#This will create an error to reflect that the interest would be higher than the monthly payment

loan_500_pay_1_int_05 = calculate_loan(500, 0.05, 1, 0)

test_p500_r5_mp1_number_of_months, test_p500_r5_mp1_total_paid = loan_500_pay_1_int_05   


#%%

assert test_p500_r5_mp100_number_of_months == 6
assert round(test_p500_r5_mp100_total_paid,2) == 506.35
assert test_p500_r5_mp500_number_of_months == 2
assert round(test_p500_r5_mp500_total_paid,2) == 502.09

#%%
#Section 3.3. We are attempting to do this for larger numbers. I was not originally getting the
#correct numbers, but I kept reworking the function to finally get the paid amount colmn to be right

loan_250000_pay_1000_int_04 = calculate_loan(250000, 0.04, 1000, 0)

length_of_loan, total_paid = loan_250000_pay_1000_int_04   
