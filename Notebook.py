# Importing the libraies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def cleaning_data():
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
    cleaned_portfolio = cleaned_portfolio.drop(['channels'],axis=1)
    
    # converting duration from days to hours for better comparision
    cleaned_portfolio['duration'] = cleaned_portfolio['duration'] * 24

    # one hot encoding the offer_type column
    ohe = pd.get_dummies(cleaned_portfolio['offer_type'])
    cleaned_portfolio = pd.concat([cleaned_portfolio,ohe],axis=1)
    cleaned_portfolio = cleaned_portfolio.drop(['offer_type'],axis=1)
    
    # renaming the id column to offer_id
    cleaned_portfolio = cleaned_portfolio.rename(columns={'id':'offer_id'})
    
    
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

    # Renaming the id column to customer_id
    cleaned_profile = cleaned_profile.rename(columns={'id':'person_id'})
    
    # OneHotEncoding the gender column
    ohe = pd.get_dummies(cleaned_profile['gender'])
    cleaned_profile = pd.concat([cleaned_profile,ohe],axis=1)
    
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
    cleaned_profile['age_by_decade'] = pd.cut(cleaned_profile['age'], bins=range(10,120,10),right=False, labels=['10s','20s', '30s', '40s', '50s','60s', '70s', '80s', '90s', '100s'])
    cleaned_profile['income_range'] = pd.cut(cleaned_profile['income'], bins=range(0,120001,10000),right=False, labels=['10k','20k', '30k', '40k', '50k','60k', '70k', '80k', '90k', '100k', '110k', '120k'])   
    
    # Data Cleaning of transcript.json
    cleaned_transcript = transcript
    
    # OneHotEncoding the event column
    ohy = pd.get_dummies(cleaned_transcript['event'])
    cleaned_transcript = pd.concat([cleaned_transcript,ohy],axis=1)
    cleaned_transcript = cleaned_transcript.drop(['event'],axis=1)
    
    # To delete all the information of the people had NULL values qhich we previously dropped.
    profile118 = profile[profile['age']==118]
    id118 = profile118['id']
    
    cleaned_transcript = cleaned_transcript[~cleaned_transcript['person'].isin(id118)]
    
    cleaned_transcript['record'] = cleaned_transcript.value.apply(lambda x: list(x.keys())[0])
    cleaned_transcript['record_value'] = cleaned_transcript.value.apply(lambda x: list(x.values())[0])
    cleaned_transcript.drop(['value'], axis=1, inplace=True)
    
    transactions = cleaned_transcript[cleaned_transcript.transaction == 1]
    offers = cleaned_transcript[cleaned_transcript.transaction != 1]
    
    # cleaning transactions
    transactions = transactions.drop(['offer completed','offer viewed','offer received'],axis=1)
    transactions = transactions.drop(['transaction','record'],axis=1)
    transactions = transactions.rename(columns={'record_value':'amount'})
    transactions['amount_range'] = pd.cut(transactions['amount'], bins=range(0,1150,50),right=False, labels=['50','100', '150', '200','250','300','350','400','450','500','550','600','650','700','750','800','850','900','950','1000','1050','1100'])   
    # cleaning offers
    offers = offers.drop(['transaction','record'],axis=1)
    offers = offers.rename(columns={'record_value':'offer_id'})

    offers['offer_type'] = offers['offer_id'].copy()

    offers['offer_type'].replace(['ae264e3637204a6fb9bb56bc8210ddfd','4d5c57ea9a6940dd891ad53e9dbe8da0',\
                                 '9b98b8c7a33c4b65b9aebfe6a799e6d9','f19421c1d4aa40978ebb69ca19b0e20d'],\
                                 'bogo', inplace=True)

    offers['offer_type'].replace(['0b1e1539f2cc45b7b9fa7c272da2e1d7','2298d6c36e964ae4a3e7e9706d1fb8c2',\
                                 'fafdcd668e3743c1bb461111dcafc2a4','2906b810c7d4411798c6938adc9daaa5'],\
                                 'discount', inplace=True)

    offers['offer_type'].replace(['3f207df678b143eea3cee63160fa8bed','5a8bc65990b245e5a138643cd4eb9837'],\
                                 'informational', inplace=True)
    
    return cleaned_portfolio, cleaned_profile, offers, transactions
