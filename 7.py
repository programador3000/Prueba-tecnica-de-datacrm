from hashlib import md5
from lib2to3.pgen2 import token
import re
from sre_constants import SUCCESS
from unittest import result
from flask import render_template
from matplotlib.pyplot import get
import requests
import json
import hashlib
from flask import render_template,Flask, Response
app = Flask(__name__)
app.debug=True
def gettoken():
    api_url = "https://develop.datacrm.la/anieto/anietopruebatecnica/webservice.php?operation=getchallenge&username=prueba"
    response = requests.get(api_url)
    lol = response.json()
    print (lol)
    diccionario1 =  lol['result']
    token = diccionario1['token']
    print(token)
    return token
# initializing string

token=gettoken();
  
# encoding GeeksforGeeks using encode()
# then sending to md5()
def hacer_hash(token,clave):
    hash = hashlib.md5((token+clave).encode('utf-8')).hexdigest()
    accessKey = json.dumps({"md5": hash })
# printing the equivalent hexadecimal value.
    print("The hexadecimal equivalent of hash is : ", end ="")
    print(hash)
    return hash

def login():
    auth_data = {'Content-Type':'application/x-www-form-urlencoded', 'operation':'login', 'username':'prueba','accessKey': {frozenset({hacer_hash(token,'Vn4HOWtkJOsPX7t')})}}
    resp = requests.post("https://develop.datacrm.la/anieto/anietopruebatecnica/webservice.php", data=auth_data)
    print(resp.json())
    print(resp.status_code)
    lola=resp.json()
    resultsesion = lola['result']
    resultadolola=resultsesion['sessionName']
    return resultadolola
  
    


def data():
    url3=f"https://develop.datacrm.la/anieto/anietopruebatecnica/webservice.php?operation=query&sessionName={login()}&query=select id, contact_no, lastname, createdtime from Contacts;"
    print(url3)
    consulta2 = requests.get(url3)
    print(consulta2.json())
    df=consulta2.json()
    datos=df['result']
    return datos

lol=data()

@app.route('/')
def get_data():
    informacion=lol
    print (informacion)
    return render_template("index.html", informacion=informacion)


if __name__ == '__main__':
    app.run()


