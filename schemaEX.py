
# coding: utf-8

# Creation of Schema Metadate File
# <br\>
# The metadata of the schema will be written into the [schema-"date()".csv] file. 
# <br\>
# The function below will directly read the DGS data and export it as a csv file. Just call the function to use it.
# <br\>
# <br\>
# <i>Example: `write_schema_metadata()`</i>

# In[ ]:


import datetime
import unicodecsv as csv
import packageEX as s1


# In[ ]:


def write_schema_metadata():
    
    # Get date and time
    now = datetime.datetime.now()
    created = now.strftime("%d%B%Y")
    
    # Fields to include for the resource metadata file
    fnames2 = ['resource.identifier','field','attribute','value']
    fnames = ['resource.identifier','schema.field','schema.attribute','schema.value']
    
    # Creating the csv file
    with open('schema_metadata.csv','wb') as f:
        writer = csv.DictWriter(f, fieldnames=fnames,encoding='utf-8')
        writer.writeheader()

        # Iterate through the DGS data
        for iList in range(0,len(s1.dgs_crawl)):
            package_metadata = s1.dgs_crawl[iList]
            resource_dict = package_metadata['resources']
            
            # iResource denotes the number of resources in the package
            for iResource in range(0,len(resource_dict)):
                # if schema is not present, give it a 'NA'
                if resource_dict[iResource].get('schema') is None:
                    resource_dict[iResource]['schema'] = [{'name': 'NA'}]
                # For each resource, iField denotes the number of fields in the schema
                for iField in range(0,len(resource_dict[iResource]['schema'])):
                    # List the attributes associated with each Field
                    field_attr = resource_dict[iResource]['schema'][iField].keys()
                    for iattr in field_attr:
                        # Convert unicode to utf-8
                        if isinstance(iattr,unicode):
                            iattr = iattr.encode('utf-8','replace')
                        
                        # Construct Schema dictionary
                        schema_dict = {'resource.identifier': resource_dict[iResource]['identifier'],
                                       'schema.field': iField,
                                       'schema.attribute': iattr,
                                       'schema.value': resource_dict[iResource]['schema'][iField][iattr]}
                        # Write the new dictionary into the csv file
                        writer.writerow(schema_dict)
        print "Writing Schema Metadata Complete!!"
        f.close()
        
    # Writes a log file upon success
    with open('log.txt','a') as f2:
        writer = csv.DictWriter(f2, fieldnames=['Date','Action'], encoding='utf-8')
        writer.writerow({'Date':now, 'Action':'write_schema_metadata()'})
        f2.close()

