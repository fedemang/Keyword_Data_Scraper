# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:37:53 2023

@author: Federico
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:08:18 2023

@author: Federico
"""
import requests
#import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as io
import time
import random
import re

#io.renderers.default='browser'
io.renderers.default='svg'

def StringExtractor(test_str, sub1, sub2):
    try:
    # getting elements in between using split() and join()
        res = ''.join(test_str.split(sub1)[1].split(sub2)[0])
        #res.replace(" ", "")
        return res
    #print("The extracted string : " + res)
    except Exception as e:
        return test_str
        print("some error occurred: " + e)
        
        
def NumberExtractor(test_str):
    try:
        test_str = test_str.replace("118"," ") #removes the years
        test_str = re.sub(r'(?:2100|200[1-9]|20[1-9]\d)', ' ',  test_str)#removes numbers from 2100 to 2000
        test_str = re.sub(r'(?:2000|1900[1-9]|19[1-9]\d)', ' ',  test_str)#removes numbers from 2000 to 1900
        # use the split() method to split
        # use the filter() function to filter out non-numeric elements from the list
        res = list(filter(lambda x: x.isdigit(), test_str.split()))
        res = list(set(res)) #removes duplicates     
        return res
    except Exception as e:
        return test_str
        print("some error occurred: " + e)
    # use a list comprehension to convert the remaining elements to integers
    #res = [int(s) for s in res]

def Comparison(testdf):

    df = pd.read_json(r"C:\Users\Federico\Desktop\Dati\Province_Italiane_giornali_agg.json")

#Let's separate all the list elements
    Data =[]
    Data = df['giornale']

    dummy=len(Data)

    Information1=[]
    for i in range(0,dummy):
        Information1.append(Data[i][0])
  
    Information2=[]
    for i in range(0,dummy):
        Information2.append(Data[i][1])
  
    Information3=[]
    for i in range(0,dummy):
        Information3.append(Data[i][2])
     
    Information4=[]
    for i in range(0,dummy):
        Information4.append(Data[i][3])
    
    Information5=[]
    for i in range(0,dummy):
        Information5.append(Data[i][4])

#let's create a new dataframe with them

    df1=pd.DataFrame() 
    df1["giornale1"]= Information1
    df1["giornale2"] = Information2
    df1["giornale3"] = Information3
    df1["giornale4"] = Information4
    df1["giornale5"] = Information5
    df1["provincia"] = df["nome"]


    dfinal1 = df1.merge(testdf, how='inner', left_on='giornale1', right_on='giornale')
    dfinal2 = df1.merge(testdf, how='inner', left_on='giornale2', right_on='giornale')
    dfinal3 = df1.merge(testdf, how='inner', left_on='giornale3', right_on='giornale')
    dfinal4 = df1.merge(testdf, how='inner', left_on='giornale4', right_on='giornale')
    dfinal5 = df1.merge(testdf, how='inner', left_on='giornale5', right_on='giornale')

    result = pd.concat([dfinal1, dfinal2, dfinal3, dfinal4, dfinal5]) #concatenate vertically


    df_to_map=pd.DataFrame() 
    df_to_map["Provincia"]=result["provincia"]
    df_to_map["Conta"] = result["provincia"].map(result["provincia"].value_counts())
    df_to_map = df_to_map.drop_duplicates(subset=None, keep='first', inplace=False)
    return df_to_map

def MapGenerator(your_input_data):
    
    province_geo = gpd.read_file(r'C:\Users\Federico\Desktop\Dati\Province_Confini.json')

    #Creates a dataset which contains all data needed (and something more)
    province_geo1=province_geo.merge(your_input_data, how='left', left_on='prov_name', right_on='Provincia')  
    province_geo1=province_geo1.fillna(0)

    # Load TopoJSON

    # Create center from bounding box
    bbox = [6.626621368537682, 35.493691935511414, 18.520381599098922, 47.09178374646217]
    center = {"lat": (bbox[3] + bbox[1]) / 2, "lon": (bbox[2] + bbox[0])/2}

    # Creation of the choropleth map using Plotly
    fig = px.choropleth_mapbox(province_geo1, 
                        geojson=province_geo, 
                        locations='prov_name', 
                        featureidkey='properties.prov_name',
                        color='Conta',
                        mapbox_style="carto-positron",
                        zoom=4,
                        center=center,
                        title="Risultato ricerca Malore improvviso su Bing",
                        labels={'Conta': 'Numero Defunti'})
    fig.update_geos(fitbounds="locations", visible=True)
    fig.show()
    
"""    
headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
"""
    
user_agents = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
]     
    
user_agent = random.choice(user_agents) 
headers = {'User-Agent': user_agent}   
        
    
    
    
indirizzo =[]   
params = {
         "q": "malore+improvviso", 
         #"first": 100,
         "textDecorations": True, 
         "textFormat": "HTML",
         "cc": "it", # language
         "freshness": "2024-06-07..2022-06-01", #"2023-04-01..2023-07-17", #"Day", "Week", "Month", "Year" freshness=2019-02-01..2019-05-30
         "SafeSearch":"Off", # can be "Off", "Strict" or "Moderate"
         "responseFilter": "news" 
         }     

for i in range(0,400,20):
    
    target_url="https://www.bing.com/search?q=%s&rdr=1&first={}".format(i+1)   
       
    time.sleep(30)
    #print(target_url)
    resp = requests.get(target_url, headers=headers, params=params)
    #print(resp)
    #soup = BeautifulSoup(resp.text, 'html.parser')
    soup = BeautifulSoup(resp.text, 'lxml')
    completeData = soup.find_all("li",{"class":"b_algo"})
    #print(completeData)
    for el in completeData:
        indirizzo.append(el.get_text())
        print (el.get_text())
    
    
info_morti = pd.DataFrame() 
info_morti["Indirizzo"]= indirizzo


prova =[]
prova1 =[]
prova2 = []
prova3 = []
prova4= []
age=[]
age1=[]

dummy=len(indirizzo)
for i in range(0, dummy):
    joe = StringExtractor(indirizzo[i], "www", ".it")
    prova.append(joe)
    joe1 = StringExtractor(prova[i], "www", ".com")
    prova1.append(joe1)
    joe2 = StringExtractor(prova1[i], ".", ".com")
    prova2.append(joe2)
    joe3 = StringExtractor(prova2[i], ".", ".it") #works best this way! Don't change!
    prova3.append(joe3)
    joe4 = StringExtractor(prova3[i], "//", " ") #works best this way! Don't change!
    prova4.append(joe4)
    joe_age = NumberExtractor(indirizzo[i]) #not bad
    age.append(joe_age)

#cleans the age list from some garbage
age = list(filter(None, age))#removes empty values

dummy=len(age)
for i in range(0, dummy):
    jim_age= max(age[i], key =float)
    age1.append(jim_age)



#info_morti["Indirizzo purificato"]= prova
#info_morti["Indirizzo purificato1"]= prova1
#info_morti["Indirizzo purificato2"]= prova2
info_morti["giornale"]= prova4

#this bit of code plots the histogram
df_age = pd.DataFrame() 
df_age['età morti'] = age1
#df_age = df_age.sort_values(by='età morti', ascending=True)



df_to_map = Comparison(info_morti) 

mappa = MapGenerator(df_to_map)

stat_morti = px.histogram(df_age, x = 'età morti').update_xaxes(categoryorder ="category ascending")

stat_morti.show()