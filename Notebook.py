# Importing the libraies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Importing the datasets
portfolio = pd.read_json("portfolio.json",lines=True)
profile = pd.read_json("profile.json",lines=True)
transcript = pd.read_json("transcript.json",lines=True)

# Data Cleaning of portfolio dataset
ohe = {'email':[1,1,1,1,1,1,1,1,1,1], 
       'mobile':[1,1,1,1,0,1,1,1,1,1], 
       'social':[1,1,0,0,0,1,1,1,1,0],
       'web':[0,1,1,1,1,1,1,0,1,1]}

ohx = pd.DataFrame(ohe,columns = ['email','mobile','social','web']) 

cleaned_portfolio = portfolio
cleaned_portfolio = pd.concat([portfolio,ohx],axis=1)

# Data Cleaning of profile dataset

# To check the number of NULL values in each column
# profile.isnull().sum()
'''
gender              2175
age                    0
id                     0
became_member_on       0
income              2175
'''
# Also on checking the age column against all the pts having gender and income 
# as Null we find that the corresponding age value is 118 which is quite
# unusual. So in order to cleanse the data we drop all such points.

# Dropping NULL values
cleaned_profile = profile
cleaned_profile = cleaned_profile.dropna()

# OneHotEncoding the gender column
ohe = pd.get_dummies(cleaned_profile['gender'])
cleaned_profile = pd.concat([cleaned_profile,ohe],axis=1)
cleaned_profile = cleaned_profile.drop(['gender'],axis=1)

# To convert the became_member_on to date-time stamp because the machine will not
# understand data corresponding to date in integer form.
cleaned_profile['became_member_on'] = pd.to_datetime(cleaned_profile['became_member_on'], format='%Y%m%d').dt.date

# We added a column today's date in the dataframe for refereence to calculate the no of days the customer has been a member of Starbucks
cleaned_profile['today_date'] = pd.to_datetime('20200828',format='%Y%m%d')
cleaned_profile['today_date'] = pd.to_datetime(cleaned_profile['today_date'],format='%Y%m%d').dt.date
cleaned_profile['days_of_membership'] = cleaned_profile['today_date'].sub(cleaned_profile['became_member_on'], axis=0)

# Taking a ratio of the subtracted dates to convert it into no.of.days
cleaned_profile['days_of_membership'] = cleaned_profile['days_of_membership'] / np.timedelta64(1, 'D')
cleaned_profile['became_member_on'] = pd.to_datetime(cleaned_profile['became_member_on'], format='%Y-%m-%d').dt.year

# Then we drop the reference column because it is not useful to us further analysis
cleaned_profile = cleaned_profile.drop(['today_date'],axis=1)
