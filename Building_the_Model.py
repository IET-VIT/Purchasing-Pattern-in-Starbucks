# Importing the libraies
import Notebook
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

cleaned_portfolio, cleaned_profile, offers, transactions = Notebook.cleaning_data()


# Resetting the index of varios dataframes

cleaned_profile = cleaned_profile.reset_index()
cleaned_profile = cleaned_profile.drop(['index'], axis=1)

offers = offers.reset_index()
offers = offers.drop(['index'], axis=1)

transactions = transactions.reset_index()
transactions = transactions.drop(['index'], axis=1)



# Create function to combine transaction, offer, portfolio and profile datasets

    
combined_data = [] # Initialize empty list for combined data
customer_id_list = offers['person'].unique().tolist() # List of unique customers in offers_df
    

# Iterate over each customer
for i,cust_id in enumerate(customer_id_list):
        
    # select customer profile from profile data
    cust_profile = cleaned_profile[cleaned_profile['person_id'] == cust_id] 
    
    # select offers associated with the customer from offers_df
    cust_offers_data = offers[offers['person'] == cust_id]
    
    # select transactions associated with the customer from transactions_df
    cust_transaction_df = transactions[transactions['person'] == cust_id]
    
    # select received, completed, viewed offer data from customer offers
    offer_received_data  = cust_offers_data[cust_offers_data['offer received'] == 1]
    offer_viewed_data = cust_offers_data[cust_offers_data['offer viewed'] == 1]
    offer_completed_data = cust_offers_data[cust_offers_data['offer completed'] == 1]
        
    # Iterate over each offer received by a customer
    rows = [] # Initialize empty list for a customer records
        
    for off_id in offer_received_data['offer_id'].values.tolist():
        
        # select duration of a particular offer_id
        duration = cleaned_portfolio.loc[cleaned_portfolio['offer_id'] == off_id, 'duration'].values[0]
        
        # select the time when offer was received
        off_recd_time = offer_received_data.loc[offer_received_data['offer_id'] == off_id, 'time'].values[0]
        
        # Calculate the time when the offer ends
        off_end_time = off_recd_time + duration
        
        #Initialize a boolean array that determines if the customer viewed an offer between offer period
        offers_viewed = np.logical_and(offer_viewed_data['time'] >= off_recd_time,offer_viewed_data['time'] <= off_end_time)
            
        # Check if the offer type is 'bogo' or 'discount'
        if (cleaned_portfolio[cleaned_portfolio['offer_id'] == off_id]['bogo'].values[0] == 1 or\
                cleaned_portfolio[cleaned_portfolio['offer_id'] == off_id]['discount'].values[0] == 1):
            
            #Initialize a boolean array that determines if the customer completed an offer between offer period
            offers_comp = np.logical_and(offer_completed_data ['time'] >= off_recd_time,\
                                             offer_completed_data ['time'] <= off_end_time)
                
            #Initialize a boolean array that selects customer transctions between offer period
            cust_tran_within_period = cust_transaction_df[np.logical_and(cust_transaction_df['time'] >= off_recd_time,\
                                                                             cust_transaction_df['time'] <= off_end_time)]
                
            # Determine if the customer responded to an offer(bogo or discount) or not
            cust_response = np.logical_and(offers_viewed.sum() > 0, offers_comp.sum() > 0) and\
                                                (cust_tran_within_period['amount'].sum() >=\
                                                 cleaned_portfolio[cleaned_portfolio['offer_id'] == off_id]['difficulty'].values[0])
            
        # Check if the offer type is 'informational'
        elif cleaned_portfolio[cleaned_portfolio['offer_id'] == off_id]['informational'].values[0] == 1:
            
            #Initialize a boolean array that determines if the customer made any transctions between offer period
            cust_info_tran = np.logical_and(cust_transaction_df['time'] >= off_recd_time,\
                                                cust_transaction_df['time'] <= off_end_time)                   
                
            # Determine if the customer responded to an offer(informational) or not
            cust_response = offers_viewed.sum() > 0 and cust_info_tran.sum() > 0                  
            
            #Initialize a boolean array that selects customer transctions between offer period
            cust_tran_within_period = cust_transaction_df[np.logical_and(cust_transaction_df['time'] >= off_recd_time,\
                                                                             cust_transaction_df['time'] <= off_end_time)]
            
        # Initialize a dictionary for a customer with required information for a particular offer
        cust_rec = {'cust_response': int(cust_response),'time': off_recd_time,'total_amount': cust_tran_within_period['amount'].sum()}
        cust_rec.update(cleaned_profile[cleaned_profile['person_id'] == cust_id].squeeze().to_dict())
        cust_rec.update(cleaned_portfolio[cleaned_portfolio['offer_id'] == off_id].squeeze().to_dict())
            
        # Add the dictionary to list for combined_data
        rows.append(cust_rec)
        
    # Add the dictionaries from rows list to combined_data list
    combined_data.extend(rows)
        
    
# Convert combined_data list to dataframe
combined_data_df = pd.DataFrame(combined_data)
    
# Reorder columns of combined_data_df
combined_data_df_col_order = ['person', 'offer_id', 'time']

port_ls = cleaned_portfolio.columns.tolist()
port_ls.remove('offer_id')
pro_ls = cleaned_profile.columns.tolist()
pro_ls.remove('person_id')
combined_data_df_col_order.extend(port_ls)
combined_data_df_col_order.extend(pro_ls)
combined_data_df_col_order.extend(['total_amount', 'cust_response'])
    
combined_data_df = combined_data_df.reindex(combined_data_df_col_order, axis=1)
combined_data_df = combined_data_df.drop(['person'],axis=1)

model_df = combined_data_df
e = pd.get_dummies(model_df['became_member_on'])
model_df = pd.concat([model_df,e],axis=1)
f = pd.get_dummies(model_df['age_by_decade'])
model_df = pd.concat([model_df,f],axis=1)
g = pd.get_dummies(model_df['income_range'])
model_df = pd.concat([model_df,g],axis=1)


model_df = model_df.drop(['offer_id','age','income','email','time', 'gender', 'age_by_decade','became_member_on', 'income_range'], axis=1)
model_df.to_csv('model_data.csv', index=False)



X = model_df.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38]].values
y = model_df.iloc[:,14].values

# Splitting the data into training and test
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42)

# Standard scaling the required columns
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Now fitting the data into the best classifier

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                   criterion='gini', max_depth=None, max_features='auto',
                   max_leaf_nodes=None, max_samples=None,
                   min_impurity_decrease=0.0, min_impurity_split=None,
                   min_samples_leaf=1, min_samples_split=5,
                   min_weight_fraction_leaf=0.0, n_estimators=80,
                   n_jobs=None, oob_score=False, random_state=42, verbose=0,
                   warm_start=False)
classifier.fit(X_train,y_train)

'''from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=25,metric='minkowski',p=2)
classifier.fit(X_train,y_train)'''


# Making the predictions
y_pred = classifier.predict(X_test)

# Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
acc = (cm[0][0]+cm[1][1])/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])

    
filename = 'model.sav'
pickle.dump(classifier, open(filename, 'wb'))
 
# some time later...
 
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)


X = model_df.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38]].values
y = model_df.iloc[:,14].values

# Splitting the data into training and test
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42)

# Standard scaling the required columns
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                       criterion='entropy', max_depth=None, max_features='auto',
                       max_leaf_nodes=None, max_samples=None,
                       min_impurity_decrease=0.0, min_impurity_split=None,
                       min_samples_leaf=2, min_samples_split=5,
                       min_weight_fraction_leaf=0.0, n_estimators=500,
                       n_jobs=None, oob_score=False, random_state=42, verbose=0,
                       warm_start=False)
classifier.fit(X_train,y_train)

'''from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=25,metric='minkowski',p=2)
classifier.fit(X_train,y_train)'''


# Making the predictions
y_pred = classifier.predict(X_test)

# Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

acc = (cm[0][0]+cm[1][1])/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])


filename = 'alt_model.sav'
pickle.dump(classifier, open(filename, 'wb'))

