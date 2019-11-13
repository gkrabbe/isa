#!/usr/bin/env python
# coding: utf-8

import time
from requests import Session
from signalr import Connection

# In[2]:

input("press ENTER to start CENT")

session = Session()
connection = Connection("http://127.0.0.1:8088/signalr", session)
chat = connection.register_hub('isaHub')

print("started")

# In[3]:


lamps = {"sala1": {
            "status":False,
            "timer": 0
        },
        "sala2": {
            "status":False,
            "timer": 0
        },
        "cozinha": {
            "status":False,
            "timer": 0
        },
        "quarto1": {
            "status":False,
            "timer": 0
        },
        "quarto2": {
            "status":False,
            "timer": 0
        },
        "fora": {
            "status":False,
            "timer": 0
        },
        "corredor": {
            "status":False,
            "timer": 0
        },
        "banheiro": {
            "status":False,
            "timer": 0
        },
        "servico": {
            "status":False,
            "timer": 0
        }}


# In[4]:


def statusLocalization(name, status):
    _name = name[1:]
    
    for lamp in lamps:
        if(lamp == _name):
            lamps[lamp]={"status":True,"timer": 6}
        else:
            lamps[lamp]["status"]=False       


# In[5]:


chat.client.on('statusLocalization', statusLocalization)
connection.start()


# In[ ]:


with Session() as session:    
    with connection:
        while True:            
            for name,value in lamps.items():
                if(value["status"]):
                    print('sendLamp',name, True)
                    chat.server.invoke('sendLamp',name, True)                    
                elif(value["timer"]==1):
                    print('sendLamp',name, False)
                    chat.server.invoke('sendLamp',name, False)
                    lamps[name]["timer"]-=1
                else:                    
                    lamps[name]["timer"]-=1                    
            connection.wait(1)




