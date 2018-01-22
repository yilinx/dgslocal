
# coding: utf-8

# Creation of Resource Metadata File
# <br\>
# The metadata of the resources will be written into the [resource_metadata-"date()".csv] file.
# <br\>
# The function below will directly read the DGS data and export it as a csv file. Just call the function to use it.
# <br\>
# <br\>
# <i>Example: `write_resource_metadata()`</i>

# In[ ]:


import datetime
import unicodecsv as csv
import packageEX as s1


# In[ ]:


def write_resource_metadata():
    
    # Get date and time
    now = datetime.datetime.now()
    created = now.strftime("%d%B%Y")
    
    # Fields to include for the resource metadata file
    fnames = ['resource.coverage','resource.format','pkg.id','resource.identifier','resource.last_updated','resource.title','resource.url']
    fnames2 = ['coverage','format','pkg.id','resource.identifier','last_updated','title','url']
    
    # Creating the csv file
    with open('resource_metadata.csv','wb') as f:
        writer = csv.DictWriter(f, fieldnames=fnames, encoding='utf-8')
        writer.writeheader()

        # Iterate through the DGS listing
        for iList in range(0,len(s1.dgs_crawl)):
            package_metadata = s1.dgs_crawl[iList]
            resource_dict = package_metadata['resources']
            
            # iResource denotes the number of resources in the package
            for iResource in range(0,len(resource_dict)):
                # Insert NA for missing fields and change remaining text to utf-8 to avoid error
                for element in fnames2:
                    if resource_dict[iResource].get(element) is None:
                        resource_dict[iResource][element] = 'NA'
                    else:
                        if isinstance(resource_dict[iResource][element],unicode):
                            resource_dict[iResource][element] = resource_dict[iResource][element].encode('utf-8')

                # Construct metadata dictionary for each resource
                new_resource_meta_dict = {'resource.coverage': resource_dict[iResource]['coverage'],
                                          'resource.format': resource_dict[iResource]['format'],
                                          'pkg.id': package_metadata['identifier'],
                                          'resource.identifier': resource_dict[iResource]['identifier'],
                                          'resource.last_updated': resource_dict[iResource]['last_updated'],
                                          'resource.title': resource_dict[iResource]['title'],
                                          'resource.url': resource_dict[iResource]['url']}

                # Write the new dictionary into the csv file
                writer.writerow(new_resource_meta_dict)
        print "Writing Resource Metadata Complete!!"
        f.close()
        
    # Writes a log file upon success
    with open('log.txt','a') as f2:
        writer = csv.DictWriter(f2, fieldnames=['Date','Action'], encoding='utf-8')
        writer.writerow({'Date':now, 'Action':'write_resource_metadata()'})
        f2.close()

