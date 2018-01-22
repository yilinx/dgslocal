
# coding: utf-8

# Weekly automator
# 
# For a weekly update, if the date difference between reference date and today is a multiple of 7 (% 7 == 0), it will run the script.
# <br\>
# This script will run a pipeline that extracts DGS metadata and convert it to TDE format before emailing users.

# In[ ]:


#!/usr/bin/python2.7

import datetime

# d1 is the reference date to run the extraction scripts. Ideally should be Saturday wee hours.
d1 = datetime.date(2018,1,20)
d2 = datetime.date.today()

diff = d2-d1

if diff.days % 2 == 0:
    print "Start Data Extraction!!"
    import pipelinetde
else:
    print "Not running script today."

