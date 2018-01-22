
# coding: utf-8

# Construction of Tableau Extract
# <br\>
# In this function, the merged data is converted into a Tableau Data Extract and zipped up. This is to further reduce the footprint of the file.
# <br\>
# <br\>
# This module uses the Data Extract API in Tableau SDK.
# <br\>
# <i>https://onlinehelp.tableau.com/current/api/sdk/en-us/SDK/tableau_sdk_installing.htm</i>

# In[ ]:


# Check if the previous tde, zip and log file exist. If so, remove it.

from pathlib2 import Path
import os
import unicodecsv as csv

filechk = ['DGSextract.tde','DataExtract.log','DGS-extract.zip']

for ifile in filechk:
    my_file = Path(ifile)
    if my_file.is_file():
        os.remove(ifile)


# In[ ]:


# get 'dataextract' package for your python installation from http://www.tableau.com/data-extract-api
# script tested on Python 2.7 - 32 bit instance on Windows 10
# By Ashish Chauhan | originally published on http://doingdata.org/blog
# follow on http://twitter.com/ashishyoungy for more

# step 01 import requirements
# #########################################################
import pandas
import tableausdk.Extract as tde
import tableausdk as tsdk
import datetime
import zipfile

# step 02 get the data into python
# #########################################################
dataset = pandas.read_csv('pkg-resource.csv')
cheader = dataset.columns.values

# step 03 create a blank extract
# #########################################################
dataExtract = tde.Extract('DGSextract.tde')

# step 04 define schema
# #########################################################
dataSchema = tde.TableDefinition()

for item in cheader:
    if item.find('last_updated') >= 0:
        dataSchema.addColumn(item,tsdk.Types.Type.DATETIME)
    elif item == 'sn':
        dataSchema.addColumn(item,tsdk.Types.Type.INTEGER)
    else:
        dataSchema.addColumn(item,tsdk.Types.Type.CHAR_STRING)
        
# step 05 connect schema with blank extract
# #########################################################
table = dataExtract.addTable('Extract',dataSchema)

# step 06 fill extract with data
# #########################################################

newRow = tde.Row(dataSchema)

for i in range(0, len(dataset)):
    for nitem in range(0,len(cheader)):
        if cheader[nitem].find('last_updated') >= 0:
            try:
                dt = datetime.datetime.strptime(dataset[cheader[nitem]][i],'%Y-%m-%dT%H:%M:%S.%f')
                newRow.setDateTime(nitem, dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,0)
            except ValueError:
                dt = datetime.datetime.strptime(dataset[cheader[nitem]][i],'%Y-%m-%dT%H:%M:%S')
                newRow.setDateTime(nitem, dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,0)
                
        elif cheader[nitem] == 'sn':
            newRow.setInteger(nitem,dataset[cheader[nitem]][i])
        else:
            try:
                newRow.setCharString(nitem,dataset[cheader[nitem]][i])
            except TypeError:
                newRow.setNull(nitem)
    table.insert(newRow)

 # step 07 close the extract
# #########################################################
dataExtract.close()   


 # Step 8 Zip the file up
# #########################################################
zf = zipfile.ZipFile('DGS-extract.zip', mode='w')
zf.write('DGSextract.tde')
zf.close()

print "TDE creation is completed and file zipped"
now = datetime.datetime.now()

 # Writes a log file upon success
with open('log.txt','a') as f2:
    writer = csv.DictWriter(f2, fieldnames=['Date','Action'], encoding='utf-8')
    writer.writerow({'Date':now, 'Action':'dataExtract()'})
    f2.close()

