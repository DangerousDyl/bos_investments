#!/usr/bin/env python
# coding: utf-8

# ## 1: Setting Up DF1
# 
# #### 1.1: Importing Modules

# In[1]:


import os
import pandas as pd 
import numpy as np 
import matplotlib as plt 
import seaborn as sns    #not required until graphing
from datetime import datetime
import matplotlib.pyplot as plt
sns.set


# #### 1.2: Adjusting Directory

# In[2]:


env = os.chdir(r'C:\Users\alexb\OneDrive\Documents\02 - Work\coding\TimeSeries')
path = os.getcwd()
path


# #### 1.3: Importing Data

# In[3]:


df1 = pd.read_csv("s&p500_data.csv", infer_datetime_format = True)
df1.head(6)


# #### 1.4- Adjusting for inflation
# 
# https://timeseriesreasoning.com/contents/inflation-adjustment/#:~:text=The%20formula%20for%20inflation%20adjustment,multiplying%20the%20result%20by%20100.

# In[4]:


df1["price"] = df1["SP500"]/df1["Consumer Price Index"]*100
df1.head(6)


# #### 1.5: Isolating relevant variables

# In[5]:


exclusions = ["Dividend","Earnings","Real Dividend","Real Earnings","Real Price","Long Interest Rate","PE10","Consumer Price Index","SP500"]
i = 0
while i < len(exclusions):
    df1.drop(exclusions[i], inplace=True, axis=1)
    i = i + 1

df1.head(6)


# ## 2: Setting up DF2

# #### 2.1 : Create list to iterate over

# In[6]:


date_list = pd.to_datetime(df1['Date'])
print(date_list.head(6))

rows = len(date_list) 
rows      # to give us the number of times we need to run the loop


# #### 2.2: Define bins

# In[7]:


months_in_year = 12
years_in_window = 15
bin_size = months_in_year * years_in_window
bin_size


# #### 2.3 : Define bin-creation function

# In[8]:


def make_list(start):
    list1 = []
    end = start + bin_size
    i = 0
    for i in range(rows):
        if i < start or i > end:
            list1.append(0)
            i = i + 1
        else:
            dummy = df1.iloc[i,1]
            list1.append(dummy)
            i = i + 1
    return list1


# #### 2.4 - Testing the function (works)

# In[9]:


#list1 = make_list(10)
#print(list1) 


# #### 2.5 - Create DF2

# In[10]:


#df2 = pd.DataFrame()
#df2.insert(0,1,list1)

#df2.head(20) # Works


# In[11]:


df2 = pd.DataFrame()

for i in range(rows):
    list1 = make_list(i)
    df2.insert(i,i,list1)

df2.head(5)


# ## 3 - Analysing the data

# #### 2.1. Generating list of end values
# We have a list with all of the starting values (df1). We want to find the final value to be able to find compound growth, so we shift each index forward 180 to get the ending value

# In[26]:


start_values = []

i = 0

for i in range(rows):
    start_index = i - bin_size
    if start_index > 0:
        dummy = df1.iloc[start_index,1]
        start_values.append(dummy)
        i = i + 1
    else:
        start_values.append(0)
        i = i + 1

#print(start_values) #Works. This will be appended to dataframe


# In[31]:


df1["start price"] = start_values
df1.head(185)


# #### CAGR
# ![image.png](attachment:4a671684-f317-4096-bca6-97b94b7b400b.png)
# 

# In[32]:


df1["cagr"] = (((df1["price"]/df1["start price"])**(1/years_in_window))-1)*100
df1["Date"] = pd.to_datetime(df1["Date"])
df1.set_index('Date', inplace=True)


df1.head(185)


# In[51]:


plt.plot(df1["cagr"], marker="o", ms=1.5)

# Labelling 

plt.xlabel("Date")
plt.ylabel("CAGR")
plt.title("Historical CAGR")

#plt.xlim([datetime.date(1886, 1, 1), datetime.date(2018, 1, 1)])
plt.ylim(-20,20)

# Display

plt.show()


# In[ ]:



    
    


# Zeros are affecting the chart (because of the last 180 values

# In[ ]:



dtype: int64


# #### Appendix: Data Structures
# - *df1*: contains original SnP data, indexed by date (pd)
# - *date_list*: list containing only the (list)
# - *df2*: list containing final data in rolling periods
# - *list1*: temporary list storing values for a single column in df2
# 
# 
# 
# #### Variables
