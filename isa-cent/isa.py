#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np

from requests import Session
from signalr import Connection


# In[2]:


session = Session()
connection = Connection("http://127.0.0.1:8088/signalr", session)
chat = connection.register_hub('isaHub')
connection.start()


# In[3]:


lamps = dict()

def statusLocalization(name, status):
    if(status):
        lamps = {n:False for n,_ in lamps.items()}
    lamps[name[1:]]=status
    
    for n,s in lamps.items():
        chat.client.on('SendLamp', n, s)
        print('SendLamp', n, s)

def statusLamp(name, status):
    if(status):
        lamps = {n:False for n,_ in lamps.items()}
    lamps[name[1:]]=status
    
    for n,s in lamps.items():
        chat.client.on('SendLamp', n, s)
        print('SendLamp', n, s)


# In[4]:


chat.client.on('statusLocalization', statusLocalization)
chat.client.on('statusLamp', statusLamp)


# In[5]:


import time


# In[ ]:


with connection:
    while True:
        time.sleep(1)


# In[ ]:




