#!/usr/bin/env python
# coding: utf-8

# In[10]:


from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup
from datetime import date
import numpy as np
import mysql.connector

degaliniuUrlSarasas=['https://www.kuro-kainos.lt/degalu-kainos/viada','https://www.kuro-kainos.lt/degalu-kainos/takuras','https://www.kuro-kainos.lt/degalu-kainos/stateta','https://www.kuro-kainos.lt/degalu-kainos/skulas','https://www.kuro-kainos.lt/degalu-kainos/saurida','https://www.kuro-kainos.lt/degalu-kainos/orlen','https://www.kuro-kainos.lt/degalu-kainos/neste','https://www.kuro-kainos.lt/degalu-kainos/jozita','https://www.kuro-kainos.lt/degalu-kainos/emsi','https://www.kuro-kainos.lt/degalu-kainos/ecoil','https://www.kuro-kainos.lt/degalu-kainos/circle-k','https://www.kuro-kainos.lt/degalu-kainos/baltic-petroleum','https://www.kuro-kainos.lt/degalu-kainos/abromika','https://www.kuro-kainos.lt/degalu-kainos/alausa']
for page in degaliniuUrlSarasas:
    a = requests.get(page)
    soup = BeautifulSoup(a.content, 'html.parser')
#ADRESAS
    degaliniuAdresaiList = []
    degaliniuAdresai = soup.find_all('span', class_='address')
    length = len(degaliniuAdresai)
    for x in range(length):
        adresas = f"{degaliniuAdresai[x].text}"
        degaliniuAdresaiList.append(adresas.replace("\n",""))
    
    degalinesPavadinimasList = []
    degalinesPavadinimas = soup.find_all('b')[0].get_text()
    print("Degalines pavadinimas: "+degalinesPavadinimas)
    for x in range(length):
        degalinesPavadinimasList.append(degalinesPavadinimas.replace("\n",""))
#MIESTAS        
    degalinesMiestasList = []
    results = soup.find_all('span', class_='address')
    length = len(results)
    lengthNum = len(results)
    for x in range(length):
        a = f"{results[x].text}"
        array = a.split()
        miestas = array[-1]
        if miestas == "r.":
            miestas = array[-2]
            print(miestas)
            degalinesMiestasList.append(miestas.replace("\n",""))
        else:
            miestas = array[-1]
            print(miestas)
            degalinesMiestasList.append(miestas.replace("\n",""))
    
#DABARTINE DIENA
    laikoList = []
    today = date.today()
    laikas = str(today)
    for x in range(length):
        #print(laikas)
        laikoList.append(laikas.replace("\n",""))
    
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
    KainuListas = w_train.reshape(lengthNum,3)
    Kainynas = np.array(KainuListas).tolist()
    print(Kainynas)
    
    finalList = [list(a) for a in zip(degalinesMiestasList,degalinesPavadinimasList,degaliniuAdresaiList,laikoList)]
    finaleList = [a + b for a, b in zip(finalList, Kainynas)]
    listass=str(tuple(finaleList))
    newListas = listass.replace('[','(').replace(']',')')

    if lengthNum != 1:
        pagrList = newListas.replace('(', '', 1)[::-1].replace(')', '', 1)[::-1].replace("' '","'0.00'")
        print(pagrList)
    elif lengthNum == 1:
        pagrList = newListas.replace('(', '', 1)[::-1].replace(')', '', 1)[::-1].replace("' '","'0.00'").replace("),",")")
        print(pagrList)
    
    try:
        if(lengthNum != 0):
            conn = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='degalinesdb')
            cur=conn.cursor()
    
            degaliniuAdresaiListToString = str(degaliniuAdresaiList)
            listReplaceDGadress = degaliniuAdresaiListToString.replace('[', '(', 1)[::-1].replace(']', ')', 1)[::-1]
    
            sqlDeleteRows= r'DELETE FROM tbldegalinesinfo WHERE adresas in {0}'.format(listReplaceDGadress)
            cur.execute(sqlDeleteRows,listReplaceDGadress)
            print("Degalines, kurios buvo atnaujintos:\n")
            print(listReplaceDGadress)
    
            sql = r'INSERT INTO tbldegalinesinfo (miestas, pavadinimas, adresas,ikelimoData ,benzinoKaina, dyzelioKaina, dujuKaina)VALUES  {0}'.format(pagrList)
            cur.execute(sql,pagrList)
            
            conn.commit()
            print("\n Duomenys, kurie ikelti i DB:  \n")
            print(pagrList)
            #mechanizmas, kuris istraukia koordinates ir istato jas i duomenu baze
            for address in degaliniuAdresaiList:
                geolocator = Nominatim(user_agent="Your_Name")
                location = geolocator.geocode(address)
                if address==None or location==None:
                    print(address)
                    print("NERA TOKIO ADRESO")
                else:
                    a = address
                    longtitude = location.longitude
                    latitude=location.latitude
                    insert = r'INSERT INTO tbldegalineslocation (adresas, longtitude, latitude)VALUES  (%s,%s,%s)'
                    val = (a,longtitude,latitude)
                    print(val)
                    cur.execute(insert,val)
                    conn.commit()
                    
            print("-----------NAUJA DEGALINE-----------")
            conn.close()
        elif(lengthNum == 0):
            print("Nera duomenu!")
            print("-----------NAUJA DEGALINE-----------")
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
             conn.close()


# In[28]:





# In[44]:





# In[ ]:




