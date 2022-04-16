#!/usr/bin/env python
# coding: utf-8

# In[30]:


import requests
page = requests.get('https://www.kuro-kainos.lt/degalu-kainos/circle-k')
from bs4 import BeautifulSoup
import psycopg2
from datetime import date
import numpy as np

degaliniuUrlSarasas=['https://www.kuro-kainos.lt/degalu-kainos/viada','https://www.kuro-kainos.lt/degalu-kainos/takuras','https://www.kuro-kainos.lt/degalu-kainos/stateta','https://www.kuro-kainos.lt/degalu-kainos/skulas','https://www.kuro-kainos.lt/degalu-kainos/saurida','https://www.kuro-kainos.lt/degalu-kainos/orlen','https://www.kuro-kainos.lt/degalu-kainos/neste','https://www.kuro-kainos.lt/degalu-kainos/jozita','https://www.kuro-kainos.lt/degalu-kainos/emsi','https://www.kuro-kainos.lt/degalu-kainos/ecoil','https://www.kuro-kainos.lt/degalu-kainos/circle-k','https://www.kuro-kainos.lt/degalu-kainos/baltic-petroleum','https://www.kuro-kainos.lt/degalu-kainos/abromika','https://www.kuro-kainos.lt/degalu-kainos/alausa']
for page in degaliniuUrlSarasas:
    a = requests.get(page)
    soup = BeautifulSoup(a.content, 'html.parser')

    degaliniuAdresaiList = []
    #print("\nVISOS DEGALINES:")
#soup.find_all('div', class_='row days-19')
    degaliniuAdresai = soup.find_all('span', class_='address')
    length = len(degaliniuAdresai)
    for x in range(length):
        adresas = f"{degaliniuAdresai[x].text}"
        adresasPirmas = f"{degaliniuAdresai[0].text}"
        #print(adresas)
        degaliniuAdresaiList.append(adresas.replace("\n",""))
    
    degalinesPavadinimasList = []
    degalinesPavadinimas = soup.find_all('b')[0].get_text()
    print("Degalines pavadinimas: "+degalinesPavadinimas)
    for x in range(length):
        #print(degalinesPavadinimas)
        degalinesPavadinimasList.append(degalinesPavadinimas.replace("\n",""))
        
    degalinesMiestasList = []
 #print("\nVISI MIESTAI:")
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
    
    #print("\nVISOS KAINOS:")
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
    
    
    finalList = [list(a) for a in zip(degalinesMiestasList,degalinesPavadinimasList,degaliniuAdresaiList,laikoList)]
#print(finalList)

    finaleList = [a + b for a, b in zip(finalList, Kainynas)]
#print(finaleList)

    listass=str(tuple(finaleList))
#print(listass)

    newListas = listass.replace('[','(').replace(']',')')
#print("newka listas: "+newka)

    if lengthNum != 1:
        pagrList = newListas.replace('(', '', 1)[::-1].replace(')', '', 1)[::-1].replace("' '","'0.00'")
        print(pagrList)
    elif lengthNum == 1:
        pagrList = newListas.replace('(', '', 1)[::-1].replace(')', '', 1)[::-1].replace("' '","'0.00'").replace("),",")")
        print(pagrList)

    hostname = 'localhost'
    database = 'postgres'
    username = 'postgres'
    pwd = '0000'
    port_id=5432
    
    try:
        if(lengthNum != 0):
            print("Prisijungta prie "+database+" duomenu bazes!\n")
            conn = psycopg2.connect(host = hostname, dbname = database, user = username, password = pwd, port = port_id)
            cur=conn.cursor()
    
        #print(degaliniuAdresaiList)
            degaliniuAdresaiListToString = str(degaliniuAdresaiList)
            listReplaceDGadress = degaliniuAdresaiListToString.replace('[', '(', 1)[::-1].replace(']', ')', 1)[::-1]
        #print(listReplaceDGadress)
    
            sqlDeleteRows= r'DELETE FROM public."tblDegalinesInfo" WHERE adresas in {0}'.format(listReplaceDGadress)
            cur.execute(sqlDeleteRows,listReplaceDGadress)
            print("Degalines, kurios buvo atnaujintos:\n")
            print(listReplaceDGadress)
    
            sql = r'INSERT INTO public."tblDegalinesInfo"(miestas, pavadinimas, "adresas", "ikelimoData","benzinoKaina", "dyzelioKaina", "dujuKaina")VALUES  {0}'.format(pagrList)
            value = [('Test2','Test2','Test2','2022-04-08'),('Test3','Test3','Test3','2022-04-08')] 
            cur.execute(sql,pagrList) #value
    
            conn.commit()
            print("\n Duomenys, kurie ikelti i DB:  \n")
            print(pagrList)
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


# In[ ]:




