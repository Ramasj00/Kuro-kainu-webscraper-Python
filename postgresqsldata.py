#!/usr/bin/env python
# coding: utf-8

# In[209]:


import requests
page = requests.get("https://www.kuro-kainos.lt/degalu-kainos/baltic-petroleum")
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
from datetime import date
import numpy as np

degaliniuAdresaiList = []
print("\nVISOS DEGALINES:")
#soup.find_all('div', class_='row days-19')
degaliniuAdresai = soup.find_all('span', class_='address')
length = len(degaliniuAdresai)
for x in range(length):
    adresas = f"{degaliniuAdresai[x].text}"
    adresasPirmas = f"{degaliniuAdresai[0].text}"
    print(adresas)
    degaliniuAdresaiList.append(adresas.replace("\n",""))
    
degalinesPavadinimasList = []
degalinesPavadinimas = soup.find_all('b')[0].get_text()
print("Degalines pavadinimas: "+degalinesPavadinimas)
for x in range(length):
    print(degalinesPavadinimas)
    degalinesPavadinimasList.append(degalinesPavadinimas.replace("\n",""))
    
degalinesMiestasList = []
print("\nVISI MIESTAI:")
results = soup.find_all('span', class_='address')
length = len(results)
lengthNum = len(results)
for x in range(length):
    a = f"{results[x].text}"
    array = a.split()
    miestas = array[-1]
    print(miestas)
    degalinesMiestasList.append(miestas.replace("\n",""))
    
#DABARTINE DIENA
laikoList = []
today = date.today()
laikas = str(today)
for x in range(length):
    print(laikas)
    laikoList.append(laikas.replace("\n",""))
    
print("\nVISOS KAINOS:")
results = soup.find_all('div', class_='price')

rep=[]
length = len(results)
inc = 2
for x in range(length):
    a= f"{[results[x].text]}"
    if x!=inc:
        b = a.replace("['']","0.00").replace("EUR","").replace("']","").replace("['","")
        #print(b)
        rep.append(b.replace("\n",""))
    else: 
        inc=inc+4
w_train = np.array(rep)
#print (w_train)

KainuListas = w_train.reshape(lengthNum,3)
#print(KainuListas)

Kainynas = np.array(KainuListas).tolist()
print(Kainynas)


# In[193]:


finalList = [list(a) for a in zip(degalinesMiestasList,degalinesPavadinimasList,degaliniuAdresaiList,laikoList)]
#print(finalList)

finaleList = [a + b for a, b in zip(finalList, Kainynas)]
#print(finaleList)

listass=str(tuple(finaleList))
#print(listass)

newListas = listass.replace('[','(').replace(']',')')
#print("newka listas: "+newka)

#finalFinalList = newka.replace('(', '[', 1)[::-1].replace(')', ']', 1)[::-1]
#print(" finalFinalList = "+finalFinalList)

pagrList = newListas.replace('(', '', 1)[::-1].replace(')', '', 1)[::-1]
print(pagrList)


# In[194]:


import psycopg2

hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = '0000'
port_id=5432

try:
    print("Prisijungta prie "+database+" duomenu bazes!")
    conn = psycopg2.connect(host = hostname, dbname = database, user = username, password = pwd, port = port_id)
    cur=conn.cursor()
    
    sql = r'INSERT INTO public."tblDegalinesInfo"(miestas, pavadinimas, "adresas", "ikelimoData","benzinoKaina", "dyzelioKaina", "dujuKaina")VALUES  {0}'.format(finalfinalfinalList)
    #value = [('Test2','Test2','Test2','2022-04-08'),('Test3','Test3','Test3','2022-04-08')]
    #for record in finalfinalfinalList:
    cur.execute(sql,finalfinalfinalList) #value
    
    conn.commit()
    print("Ikelti sie duomenys i duomenu baze \n")
    print(pagrList)
    
    conn.close()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


# In[143]:


#print(finalfinalfinalList)

