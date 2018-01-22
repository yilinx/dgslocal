
# coding: utf-8

# This function will perform joining of the tables. Currently we are left joining the package metadata to the resource metadata.

# In[1]:


import pandas as pd
import unicodecsv as csv
import datetime

# Get date and time
now = datetime.datetime.now()

def joinsrc():
    df_a = pd.read_csv('package_metadata.csv')
    df_b = pd.read_csv('resource_metadata.csv')
    df_c = pd.merge(df_b,df_a,left_on='pkg.id',right_on='identifier',how='left')

    df_c.to_csv('pkg-resource.csv',sep=',',index_label='sn')
    
    print "Complete joining sources!!"
    
    with open('log.txt','a') as f2:
        writer = csv.DictWriter(f2, fieldnames=['Date','Action'], encoding='utf-8')
        writer.writerow({'Date':now, 'Action':'joinsrc()'})
        f2.close()

