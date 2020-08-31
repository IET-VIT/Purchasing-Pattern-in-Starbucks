import Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cleaned_portfolio, cleaned_profile, offers, transactions = Notebook.cleaning_data()

''' Exploratory Data Analysis '''

# To find out the maximum no of customer's belonging to which age group
def by_age_count(cleaned_profile):
    sns.countplot(x="age_by_decade",data=cleaned_profile, palette='rocket')
  
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
    plt.bar(x, y, color='c')


# Gender conts by membership year
def gender_by_year(cleaned_profile):    
    membership_date = cleaned_profile.groupby(['became_member_on', 'gender']).size()
    membership_date = membership_date.reset_index()
    membership_date.columns = ['became_member_on', 'gender', 'count']
    
    # plot a bar graph for age distribution as a function of gender in membership program
    plt.figure(figsize=(10, 5))
    sns.barplot(x='became_member_on', y='count', hue='gender', data=membership_date)
    plt.xlabel('Membership Start Year')
    plt.ylabel('Count');
    plt.title('Gender counts by membership year')
    

# An Overview of what income range facilitates more membership
def by_income_range(cleaned_profile):
    sns.countplot(x="income_range",data=cleaned_profile)
    
def by_member_year(cleaned_profile):
    sns.countplot(x="became_member_on",data=cleaned_profile, palette='Set3')

# Comparing the Gender-wise distribution of our customer's income
def income_by_gender(cleaned_profile):
    x = cleaned_profile[cleaned_profile['F']==1]
    y = cleaned_profile[cleaned_profile['M']==1]
    z = cleaned_profile[cleaned_profile['O']==1]
    sns.kdeplot(x['income'],label='Female')
    sns.kdeplot(y['income'],label='Male')
    sns.kdeplot(z['income'],label='Other')
    
    
# Some data visualization of events related to offers

# Some numerical data regarding the offer events
    
'''
offers['offer viewed'].value_counts()
 
0    98945
1    49860

offers['offer received'].value_counts()
 
0    82304
1    66501

offers['offer completed'].value_counts()
 
0    116361
1     32444'''

# Representaion of people who viewed and didn't view the offer on recieving the offer
def offers1():
    x = ["Viewed", "Not viewed"]
    y = [49860,16641]
    plt.pie(y, labels = x,autopct='%1.2f%%', explode=(0.0,0.1), colors=['#ff9999','#66b3ff'])
def offers2():
    x = ["Completed", "Left viewed"]
    y = [32444,17416]
    plt.pie(y, labels = x,autopct='%1.2f%%', explode=(0.0,0.1), colors = ['#99ff99','#ffcc99'])
    
