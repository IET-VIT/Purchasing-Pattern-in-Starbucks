import Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cleaned_portfolio, cleaned_profile, offers, transactions = Notebook.cleaning_data()

''' Exploratory Data Analysis '''

# To find out the maximum no of customer's belonging to which age group
def by_age_count(cleaned_profile):
    sns.countplot(x="age_by_decade",data=cleaned_profile)
  
# Gender Distribution of our customer
def by_gender_count(cleaned_profile):
    '''cleaned_profile['F'].value_counts() 
    0    8696
    1    6129
    
    cleaned_profile['M'].value_counts() 
    1    8484
    0    6341
    
    cleaned_profile['O'].value_counts() 
    0    14613
    1      212
    '''
    x = ["F", "M", "O"]
    y = [6129,8484,212]
    plt.bar(x, y)

# An Overview of what income range facilitates more membership
def by_income_range(cleaned_profile):
    sns.countplot(x="income_range",data=cleaned_profile)
    
def by_member_year(cleaned_profile):
    sns.countplot(x="became_member_on",data=cleaned_profile)

# Comparing the Gender-wise distribution of our customer's income
def income_by_gender(cleaned_profile):
    x = cleaned_profile[cleaned_profile['F']==1]
    y = cleaned_profile[cleaned_profile['M']==1]
    z = cleaned_profile[cleaned_profile['O']==1]
    sns.kdeplot(x['income'],label='Female')
    sns.kdeplot(y['income'],label='Male')
    sns.kdeplot(z['income'],label='Other')