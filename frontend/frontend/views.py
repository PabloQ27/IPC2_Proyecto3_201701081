from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
import xml.etree.ElementTree as ET
import re
import requests
from .forms import Archivo
import xmltodict
import json

endpoint = "http://127.0.0.1:4000/"
val = 0
val2 = 0
def home(request): 
    global val, val2
    if request.method == 'POST' and val == 0 :
        val = 1
        archivo2 = request.FILES['documento'].read()
        temp = archivo2
        archivo = xmltodict.parse(temp)
        json_data = json.dumps(archivo)
        #print(archivo)
        print(json_data)
        
        n = str(archivo2).replace('\\n', '\n')
        r = n.replace('\\r', '\r')
        x = r.replace('\\x', '')
        x= x.replace("'",'')
        x = x.replace('b', '', 1)
        cadena = x.replace('\\t', '    ')
        c = {"archivo_xml": cadena}  
        r = requests.post(endpoint+'doc', json = json_data) #aqui se va al back(muestra sin esto)
        return render(request, "index.html", c)
    elif val == 1 and request.method == 'GET' :
        val = 0
        r = requests.get(endpoint+'devolver')
        doc = {'xml_salida': r.text}
        print(r.text)
        return render(request, "index.html", doc)

    elif val == 0 and request.method == 'GET':
        val=0
        return render(request, "index.html")
    else:
        #doc_index = loader.get_template('index.html')
        #docin = doc_index.render()
        print('else')
        return render(request, "index.html")
 
def prueba(request):
    if val == 1:
        r = requests.get(endpoint+'prueba')
        doc = {'xml_salida': r.text}
        print(r.text + '////////////////')
        return render(request, "index.html", doc)
    else:
        return render(request, "index.html")

def carga_documento(request):
    if request.method == 'GET':
        x = requests.get(endpoint+'devolver')
        print(x.text)
        doc = {'xml_salida': x.text}  
        return render(request, "index.html", doc)
        


