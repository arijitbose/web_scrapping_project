import json
import requests
from bs4 import BeautifulSoup 
import pandas as pd
from urllib.request import urlopen
from flask import Flask,request,app,jsonify,url_for,render_template

import json
from pandas import json_normalize
from IPython.display import HTML
import os
import time

app=Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():

    try:
        data=request.json['data']
        parameter1 = str(list(data.values())[0])
        html=urlopen('https://en.wikipedia.org/wiki/'+parameter1)
        soup = BeautifulSoup(html.read(), 'html.parser')
        a=[]

        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                a.append(link.attrs['href'])
        b=[]
        c='/content/player/'
        for i in a:
            if(c in i):
                b.append(i)
       
        html2=urlopen(b[0])
        soup2 = BeautifulSoup(html2.read(), 'html.parser')
        anchors = soup2.find_all('th', {'class': 'ds-w-0 ds-whitespace-nowrap ds-min-w-max'})
        d=[]
        for anchor in anchors:
            d.append(anchor.text)
    
        e=d[0:6]
        anchors2 = soup2.find_all('td', {'class': 
                                 {'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-right',
                                  'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-right ds-font-bold'}})
        f=[]
        for anchor in anchors2:
            f.append(anchor.text)
        g=f[0:6]
        new_dict = {e[i]: g[i] for i in range(len(e))}
        print(new_dict)
        df_table = pd.DataFrame(new_dict,index=[0])
        
    
        print(df_table)
        return str(df_table)
    
      
    except Exception as e:
            print('The Exception message is: ',e)  
    

    

@app.route('/predict',methods=['POST'])
def predict():
   
    searchString = request.form.values()
    data=''.join(searchString)
    final='https://en.wikipedia.org/wiki/'+data

    html=urlopen(final)#+str(data))

    
    soup = BeautifulSoup(html.read(), 'html.parser')
    a=[]

    for link in soup.find_all('a'):
        if 'href' in link.attrs:
            a.append(link.attrs['href'])
    b=[]
    c='/content/player/'
    for i in a:
        if(c in i):
            b.append(i)
       
    html2=urlopen(b[0])
    soup2 = BeautifulSoup(html2.read(), 'html.parser')
    anchors = soup2.find_all('th', {'class': 'ds-w-0 ds-whitespace-nowrap ds-min-w-max'})
    d=[]
    for anchor in anchors:
        d.append(anchor.text)
    
    e=d[0:6]
    anchors2 = soup2.find_all('td', {'class': 
                                 {'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-right',
                                  'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-right ds-font-bold'}})
    f=[]
    for anchor in anchors2:
        f.append(anchor.text)
    g=f[0:6]
    new_dict = {e[i]: g[i] for i in range(len(e))}
    # print(new_dict)
    # df_table = pd.DataFrame(new_dict,index=[0])
    # html_final = df_table.to_html()
    
    # text_file = open("templates/result.html", "w")
    # text_file.write(html_final)
     
    # text_file.close()
    # time.sleep(5) 

   
    
    


    # return render_template("result.html",name=predict)
  
  

    return render_template("home.html",prediction_text=data+"{}".format(new_dict))

   


if __name__=="__main__":
    app.run(debug=True)