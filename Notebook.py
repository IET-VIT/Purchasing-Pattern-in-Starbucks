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

oh = pd.DataFrame(ohe,columns = ['email','mobile','social','web']) 

cleaned_portfolio = portfolio
cleaned_portfolio = pd.concat([portfolio,oh],axis=1)