
# coding: utf-8

# Define packages to import

# In[ ]:


#!/usr/bin/env python
import urllib2
import urllib
import json
import pprint
import unicodecsv as csv
import sys
import datetime


# This is a function to connect and retrieve DGS package metadata

# In[ ]:


def grab_data(package_url):
    # Make the HTTP request.
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    #url_package = 'https://data.gov.sg/api/action/package_metadata_show?id=cea-salesperson-info'

    req = urllib2.Request(url = package_url,headers = hdr)
    response = urllib2.urlopen(req)
    assert response.code == 200

    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read())

    # Check the contents of the response.
    assert response_dict['success'] is True
    result = response_dict['result']
    
    return result
    #return pprint.pprint(result)
    #pprint.pprint (result['resources'][0]['schema'])


# This object defines DGS masterlisting which will grab and list out the package ids in DGS.
# <br\>
# <br\>
# The attribute "length" defines the total number of elements in the DGS listing. Remember the listing starts from number "0" (number zero).
# <br\>
# <i>Example: `dgs_master.length`</i>
# <br\>
# <br\>
# The attribute "result" provides the package ids as a List type. Extract elements like a normal list.
# <br\>
# <i>  Example: `print dgs_master.result[5]` </i>
# <br\>(this example extracts the 6th element of the package ids as the numbering starts from zero.)

# In[ ]:


class dgs_master(object):
    
    # HTTP connection to load the list
    url = 'https://data.gov.sg/api/action/package_list'
    list_result = grab_data(url)
    
     # Class Object Attribute
    length = len(list_result)
    result = list_result 


# Construct a listing that downloads all the data from DGS for further processing

# In[ ]:


# Empty list to contain data from GDS
dgs_crawl = []

# Retrieve all data from DGSs
for iList in range(180,185):
    package_id = dgs_master.result[iList]
    url = 'https://data.gov.sg/api/action/package_metadata_show?id=' + package_id
    dgs_crawl.append(grab_data(url))


# This function will write the package metadata into a csv file. The file name will have the date created inside. 
# <br\>
# To run the function just call:
# <br\>
# <i>Example: `write_pkg_metadata()`</i>

# In[ ]:


def write_pkg_metadata():
    
    # Get date and time
    now = datetime.datetime.now()
    created = now.strftime("%d%B%Y")
    
    # List of the fields to present in the Package Metadata
    fnames = ['coverage','description','frequency','identifier','keywords','last_updated','license',
             'name','publisher','sources','title','topics','source_url']
    
    # Creating the csv file
    with open('package_metadata.csv','wb') as f:
        writer = csv.DictWriter(f, fieldnames=fnames, encoding='utf-8')
        writer.writeheader()

        # Iterate through the DGS listing
        for iList in range(0,len(dgs_crawl)):
            package_metadata = dgs_crawl[iList]

            # Insert NA for missing fields and change remaining text to utf-8 to avoid error
            for element in fnames:
                if package_metadata.get(element) is None:
                    package_metadata[element] = 'NA'
                else:
                    if isinstance(package_metadata[element],unicode):
                        package_metadata[element] = package_metadata[element].encode('utf-8')

            # Convert Keywords,Sources,Topic from List to csv
            kw_list = ",".join(package_metadata['keywords'])
            src_list = ",".join(package_metadata['sources'])
            topic_list = ",".join(package_metadata['topics'])

            # Construct new dictionary for the metadata consolidating the values into strings
            new_meta_dict = {'coverage': package_metadata['coverage'],
                            'description': package_metadata['description'],
                            'frequency': package_metadata['frequency'],
                            'identifier': package_metadata['identifier'],
                            'keywords': kw_list,
                            'last_updated': package_metadata['last_updated'],
                            'license': package_metadata['license'],
                            'name': package_metadata['name'],
                            'publisher': package_metadata['publisher']['name'],
                            'sources': src_list,
                            'title': package_metadata['title'],
                            'topics': topic_list,
                            'source_url': package_metadata['source_url']}

            # Write the new dictionary into the csv file
            writer.writerow(new_meta_dict)

    print "Writing Package Metadata Complete!!"
    f.close()

    with open('log.txt','a') as f2:
        writer = csv.DictWriter(f2, fieldnames=['Date','Action'], encoding='utf-8')
        writer.writerow({'Date':now, 'Action':'write_pkg_metadata()'})
        f2.close()

