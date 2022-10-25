import json
import requests
from bs4 import BeautifulSoup 
import pandas as pd
from urllib.request import urlopen
from flask import Flask,request,app,jsonify,url_for,render_template
# from ipynb.fs.full.spaceship_titanic_experiment import ExperimentalTransformer
import json
from pandas import json_normalize

app=Flask(__name__)
## Load the model

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
        df_table = pd.DataFrame(new_dict,index=[0])
        
        return str(df_table)
        
    except Exception as e:
            print('The Exception message is: ',e)  
    

    # return jsonify(str(output[0]))
    

@app.route('/predict',methods=['POST'])
def predict():
    try:
        data=[x for x in request.form.values()]
        parameter1=str(data[0])
    # return parameter1
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
        output=str(df_table.iloc[0,1])
        print(output)
        return render_template("home.html",prediction_text="Prediction Algerian Forest Fire is {}".format(output))
        # return str(df_table)
     
    except Exception as e:
        print(e)      
    #     output=str(df_table.iloc[0,0])
    # return new_dict 
        # return render_template("results.html",prediction_text="Matches played by player is {}".format(output))
        
   
    # return data

if __name__=="__main__":
    app.run(debug=True)