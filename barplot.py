
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import collections as col


# In[2]:

path_to_data = "C:\\Users\\toby\\Dropbox\\NSF_SBIR_Grant\\SpectroElectroChem\\SHGC_VLT_master.xlsx"


# In[3]:

# import the data as a panda dataframe
df = pd.read_excel(path_to_data,sheetname="Optical", header=1)


# In[4]:

# preview the data to make sure that it looks okay
df.head(20)


# In[5]:

# A command to easily see which devices spent the most time on the tester
namelives = df['Device Name'].value_counts(sort = False)


# In[6]:

dnames = df['Device Name'].tolist()


# In[7]:


anode = [] 
electrolyte = []
cathode = []
dates = []
# this loop splits the device name and extracts the date, anode, and cathode
for name in dnames:
    if name.count('_') >= 3: 
        bins = name.split('_');
        dates.append(bins[0])
        if bins[1] == "ito":
            cathode.append(bins[2])
            electrolyte.append(bins[3])
            try: 
                anode.append(bins[4])
            except IndexError:
                anode.append("ito")
        else:
            cathode.append(bins[1])
            electrolyte.append(bins[2])
            anode.append(bins[3])
    else:
            dates.append('BadDate')
            cathode.append('BadCathode')
            electrolyte.append('BadElectrolyte')
            anode.append('BadAnode')
    


# In[8]:

df['date']= pd.Series(dates, index=df.index)
df['cathode'] = pd.Series(cathode, index=df.index)
df['electrolyte'] = pd.Series(electrolyte, index=df.index)
df['anode'] = pd.Series(anode, index=df.index)


# In[9]:

matdf = pd.concat([df['Device Name'], df['date'], df['cathode'], df['electrolyte'], df['anode']], 
                  axis = 1, keys = ['DeviceName',
                  'date','cathode','electrolyte','anode']);
matdf = matdf.sort_index(by='DeviceName', ascending = True);
matdf = matdf.drop_duplicates(subset='DeviceName');


# In[10]:

counts = col.Counter(dnames)
counts = col.OrderedDict(sorted(counts.items()))
matdf['weeks alive'] = pd.Series([x / 3 for x in counts.values()], index=matdf.index)


# In[11]:

dcathode = pd.concat([ matdf['cathode'], matdf['weeks alive']],
                     axis = 1, keys = [ 'cathode', 'weeks alive'], )
dcathode.to_csv(path_or_buf="C:\\Users\\toby\\Dropbox\\NSF_SBIR_Grant\\aatoby1.csv")


# In[12]:

gcathode = dcathode.groupby('cathode').mean();
cmax = dcathode.groupby('cathode').max()
cmin = dcathode.groupby('cathode').min()
fig, ax = plt.subplots()
gcathode.plot(yerr=cmax-cmin,ax=ax, kind='bar')


# In[13]:

plt.show()


# In[ ]:



