#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 15:28:37 2024

@author: rajeshgogineni
"""

#%%
#first name and last name separate
first_name = "Rajesh" 
last_name  = "Gogineni"

#%%
#change string variables to completely lowercase
first_name_lowercase = "rajesh" #first name lowercase
last_name_lowercase = "gogineni" #last name lowercase

#%%
#Capitalize the first letter of each string
first_name_capitalized = first_name_lowercase.capitalize()
last_name_capitalized = last_name_lowercase.capitalize()

#%%
#concatentate strings together with a space in between
full_name = first_name_capitalized+" "+last_name_capitalized

#%%
#split string into separate pieces using the space
name_pieces = full_name.split(" ")

#%%
#check is name_pieces was output as a list
print(type(name_pieces))

#%%
#verify in another way if name_pieces is a list
print(name_pieces)

#%%
#accuracy check to make sure first name and last name are in the right places as we conduct the split
assert(name_pieces[0] == first_name_capitalized.split()[0]) # note: the double equals, `==`, tests for equality

assert(name_pieces[1] == last_name_capitalized.split()[0]) # note: the double equals, `==`, tests for equality

#%%
#Input Calculations where we define values beind the variables
lime_density_grams_per_cup = 248

grapefruit_density_grams_per_cup = 226.8

grams_per_pound	 = 453.592

oz_per_cup = 8 

ml_per_oz = 29.574

#%%
#Perform desired calculations inside of the .py file
#how many milliliters are in a US cup (of any fluid)
ml_per_cup = oz_per_cup * ml_per_oz

#the density of a lime, in grams per milliliter.
lime_density_grams_per_oz = (lime_density_grams_per_cup / oz_per_cup)
lime_density_grams_per_ml = (lime_density_grams_per_oz / ml_per_oz)

#the density of a lime, in pounds per ounce.
lime_density_pounds_per_cup = lime_density_grams_per_cup / grams_per_pound
lime_density_pounds_per_oz = lime_density_pounds_per_cup / oz_per_cup

#the density of half-and-half mixed lime grapefruit juice, in grams per cup.
mixed_density_grams_per_cup = (lime_density_grams_per_cup/2) + (grapefruit_density_grams_per_cup/2)

#the mass in grams of 3/4 of a US cup of mixed juice that is made up of 50% lime juice and 50% grapefruit juice.
mixed_mass_grams = (3/4)*mixed_density_grams_per_cup

# #the weight, in pounds, of 3/4 US cup of mixed juice that is made up of 50% lime juice and 50% grapefruit juice.
mixed_weight_pounds = mixed_mass_grams/grams_per_pound

# #the density of mixed juice that is 50% lime juice and 50% grapefruit juice in pounds per ounce.
mixed_density_pounds_per_cup = (mixed_density_grams_per_cup / grams_per_pound)
mixed_density_pounds_per_oz = (mixed_density_pounds_per_cup / oz_per_cup)

#%%

# Establishing the function and what it will return. This randomizes the initial message and terminating message
# This function also strings together the messages into initial message, names and terminating message when it is returned 

def generate_robot_message(first_name, last_name, possible_messages_init, possible_messages_term): #  <---- do not modify this line
    import random # gain access to the `random` library

    # select a random integer
    selection_init = random.randrange(len(possible_messages_init))
    selection_term = random.randrange(len(possible_messages_term))

    # extract the randomly selected init or term message part using []
    message_init = possible_messages_init[selection_init]
    message_term = possible_messages_term[selection_term]

    # construct a message using f-string formatting
    message = f"{message_init}, {first_name} {last_name}.  {message_term}" # 1️⃣ <---- Modify this line in Task 3 to also use `last_name`

    return message  #to get data out of a function, we must use the `return` keyword


#%%

# a hardcoded list of initial messages
possible_messages_init = ['greetings', 
                          'cheerio', 
                          'good day', 
                          'uh oh',
                          'hola'] # 2️⃣ <---- add a thing to the end of this list

# another hardcoded list of terminal messages
possible_messages_term = ['actually, i need to go over there now', 
                          "wait, don't i know you",
                          "this conversation is so boring",
                          "please stop talking"] # 2️⃣ <---- add a thing to this list


# 3️⃣ inputs are the lowercase names.  
message_result = generate_robot_message(first_name_capitalized, last_name_capitalized, possible_messages_init, possible_messages_term)   
#                                       ^^                     ^^  
#                                      change *these* to instead use the capitalized variables. 


